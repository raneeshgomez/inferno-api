import pprint

from nltk.tokenize import sent_tokenize
import time
import math
import operator
import collections

# Custom imports
from Verbalizer import Verbalizer
from inferno.db.Models import Recommendation
from inferno.db.MongoRepository import MongoRepository
from inferno.inference.FuzzyController import FuzzyController
from inferno.matchers.SentenceSimilarityMatcher import SentenceSimilarityMatcher
from inferno.sparql.SparqlRepository import SparqlRepository
from inferno.preprocessors.SpacyNluAnnotator import SpacyNluAnnotator


class RecommendationsController:

    def __init__(self):
        self.sparql = SparqlRepository()
        self.mongo = MongoRepository()
        # Debug logging
        self.pp = pprint.PrettyPrinter(indent=4)

    def fetch_starter_fact(self, domain="Solar System"):
        if domain == "Solar System":
            result = self.sparql.get_description_by_subject("Solar_System")
            if result == "SPARQL Error!":
                return {
                    'result': None,
                    'status': False,
                    'error': result
                }
            return {
                'result': result['results']['bindings'][0]['object']['value'],
                'status': True,
                'error': None
            }
        else:
            return {
                'result': None,
                'status': False,
                'error': 'Invalid domain'
            }

    def fetch_recommendations(self, text):
        # Execute NLU pipeline
        nlu_tick = time.perf_counter()

        # Initialize SpaCy annotator
        nlu = SpacyNluAnnotator()
        # Resolve coreferences in text
        resolved_text = nlu.resolve_corefs(text)
        # Extract concepts as named entities
        named_ents = nlu.extract_named_ents(resolved_text)
        # Tokenize resolved text into sentences
        sentences = sent_tokenize(resolved_text)

        # Filter out the most common concepts in the Spacy pipeline
        spacy_concepts = [term[0] for term in named_ents if term[1] == 'ORG' or term[1] == 'LOC' or term[1] == 'PERSON']
        entity_counter = collections.Counter(spacy_concepts)
        most_common_entities = entity_counter.most_common(2)
        similar_concepts = [most_common_entities[i][0] for i, entity in enumerate(most_common_entities)]

        nlu_tock = time.perf_counter()
        print(f"NLU done in {nlu_tock - nlu_tick:0.4f} seconds")

        # Retrieve relevant individuals by concept matching
        query_tick = time.perf_counter()

        concepts = []
        for concept in similar_concepts:
            concept = concept.replace(" ", "_")
            result = self.sparql.get_individuals_by_name_with_regex(concept)
            if result == "SPARQL Error!":
                return {
                    'result': None,
                    'status': False,
                    'error': result
                }
            if result['results']['bindings']:
                for individual in result['results']['bindings']:
                    individual_name = individual['individual']['value']
                    filtered_name = individual_name.replace("http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#", "")
                    concepts.append(filtered_name)
        if not concepts:
            return {
                'result': None,
                'status': False,
                'error': "Cannot generate recommendations! Composition is out of domain."
            }

        query_tock = time.perf_counter()
        print(f"Queried ontology in {query_tock - query_tick:0.4f} seconds")

        # Fetch sentences for retrieved concepts
        nlg_tick = time.perf_counter()

        obj_collection = []
        for concept in concepts:
            db_result = self.mongo.text_search(concept)
            if db_result['status']:
                for obj in db_result['data']:
                    obj_collection.append(obj)
            else:
                return db_result
        generated_sentences = [sent_obj.to_mongo().to_dict()['recommendation'] for sent_obj in obj_collection]

        nlg_tock = time.perf_counter()
        print(f"Fetched sentences in {nlg_tock - nlg_tick:0.4f} seconds")

        # Compute similarity score for verbalized sentences and input sentences
        # Consider only the latest 4 sentences for similarity matching to maintain consistent response times
        if len(sentences) > 4:
            considered_sentences = sentences[-4:]
        else:
            considered_sentences = sentences
        similarity_tick = time.perf_counter()

        matcher = SentenceSimilarityMatcher()
        similarity_scores = matcher.match_and_fetch_score(considered_sentences, generated_sentences)

        similarity_tock = time.perf_counter()
        print(f"Scored sentence similarity in {similarity_tock - similarity_tick:0.4f} seconds")

        # Compute fuzzy score for generated sentences
        fuzzy_tick = time.perf_counter()

        fuzzy = FuzzyController()
        fuzzy.initialize_fuzzy_engine()
        fuzzy_scores = []
        for score in similarity_scores:
            kb_score = score['kb_score']
            me_score = score['me_score']
            if math.isinf(kb_score):
                kb_score = 0
            if math.isinf(me_score):
                me_score = 0
            fuzzy_score = fuzzy.predict_fuzzy_score(kb_score, me_score)
            fuzzy_scores.append({
                "sentence": score['generated'],
                "score": fuzzy_score
            })

        fuzzy_tock = time.perf_counter()
        print(f"Fuzzy scored in {fuzzy_tock - fuzzy_tick:0.4f} seconds")

        # Remove duplicate recommendations from the list
        unique_tick = time.perf_counter()

        unique_recommendations = []
        for obj_1 in fuzzy_scores:
            for obj_2 in fuzzy_scores:
                if obj_1["sentence"] == obj_2["sentence"]:
                    if obj_1["score"] >= obj_2["score"]:
                        if not any(sentence["sentence"] == obj_1["sentence"] for sentence in unique_recommendations):
                            unique_recommendations.append(obj_1)
                    else:
                        if not any(sentence["sentence"] == obj_2["sentence"] for sentence in unique_recommendations):
                            unique_recommendations.append(obj_2)
                else:
                    continue

        unique_tock = time.perf_counter()
        print(f"Removed redundancies in {unique_tock - unique_tick:0.4f} seconds")

        # Rank scored recommendations in order of relevance
        unique_recommendations.sort(key=operator.itemgetter('score'), reverse=False)

        return {
            'result': unique_recommendations,
            'status': True,
            'error': None
        }

    def save_verbalized_recommendations(self):
        verbalizer = Verbalizer()
        recommendations = verbalizer.verbalize()
        # Spread sentence dictionary and filter out null objects
        spread_recommendations = [Recommendation(**recommendation) for recommendation in recommendations
                                  if recommendation is not None]
        # Truncate recommendations collection
        truncate_status = self.mongo.truncate_collection()
        if truncate_status['status']:
            # Batch insert recommendations
            batch_insert_status = self.mongo.batch_insert(spread_recommendations)
            return batch_insert_status
        else:
            return truncate_status


if __name__ == "__main__":
    total_tick = time.perf_counter()
    rec = RecommendationsController()
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(rec.fetch_recommendations("Mars is the fourth planet from the Sun and the second-smallest planet in the "
                                        "Solar System, after Mercury. Named after the Roman god of war, it is often "
                                        "referred to as the Red Planet because the iron oxide prevalent on its "
                                        "surface gives it a reddish appearance. Mars is a terrestrial planet with a "
                                        "thin atmosphere, having surface features reminiscent both of the impact "
                                        "craters of the Moon and the valleys, deserts, and polar ice caps of Earth. "
                                        "The rotational period and seasonal cycles of Mars are likewise similar to "
                                        "those of Earth, as is the tilt that produces the seasons. Mars is the site "
                                        "of Olympus Mons, the largest volcano and second-highest known mountain in "
                                        "the Solar System, and of Valles Marineris, one of the largest canyons in the "
                                        "Solar System. The smooth Borealis basin in the northern hemisphere covers "
                                        "40% of the planet and may be a giant impact feature. Mars has two moons, "
                                        "Phobos and Deimos, which are small and irregularly shaped. These may be "
                                        "captured asteroids, similar to 5261 Eureka, a Mars trojan. There are ongoing "
                                        "investigations assessing the past habitability potential of Mars, "
                                        "as well as the possibility of extant life. Future astrobiology missions are "
                                        "planned, including the Mars 2020 and ExoMars rovers. Liquid water cannot "
                                        "exist on the surface of Mars due to low atmospheric pressure, which is about "
                                        " 6⁄1000 that of the Earth's, except at the lowest elevations for short "
                                        "periods. The two polar ice caps appear to be made largely of water. The "
                                        "volume of water ice in the south polar ice cap, if melted, "
                                        "would be sufficient to cover the entire planetary surface to a depth of 11 "
                                        "meters (36 ft). Mars can easily be seen from Earth with the naked eye, "
                                        "as can its reddish coloring. Its apparent magnitude reaches −2.91, "
                                        "which is surpassed only by Jupiter, Venus, the Moon, and the Sun. Optical "
                                        "ground-based telescopes are typically limited to resolving features about "
                                        "300 kilometers (190 mi) across when Earth and Mars are closest because of "
                                        "Earth's atmosphere."))
    total_tock = time.perf_counter()
    print(f"Total process in {total_tock - total_tick:0.4f} seconds")

    # rec.save_verbalized_recommendations()
