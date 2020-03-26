import pprint
from functools import partial
from multiprocessing.pool import Pool

from nltk.tokenize import sent_tokenize
import time
import math
from py_stringmatching import MongeElkan
import operator

# Custom imports
from Verbalizer import Verbalizer
from inferno.db.Models import Recommendation
from inferno.db.MongoRepository import MongoRepository
from inferno.inference.FuzzyController import FuzzyController
from inferno.matchers.SentenceSimilarityMatcher import SentenceSimilarityMatcher
from inferno.models.Corpus import Corpus
from inferno.nlg.NlgEngine import NlgEngine
from inferno.sparql.SparqlRepository import SparqlRepository
from inferno.preprocessors.SpacyNluAnnotator import SpacyNluAnnotator
from inferno.preprocessors.WatsonNluAnnotator import WatsonNluAnnotator


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
        # Initialize new corpus
        corpus = Corpus(text)

        # TODO Utilize only last 3 sentences for algorithm

        # Annotate corpus for NLU purposes
        nlu = SpacyNluAnnotator(text)
        # Set resolved text to corpus
        # noinspection PyProtectedMember
        resolved_text = nlu.doc._.coref_resolved
        corpus.set_resolved_text(resolved_text)
        # Reinitialize NLU object with coreference resolved text
        nlu_resolved = SpacyNluAnnotator(resolved_text)
        named_ents = nlu_resolved.extract_named_ents()
        self.pp.pprint(named_ents)

        # Tokenize resolved text into sentences
        sentences = sent_tokenize(resolved_text)

        # Execute Watson NLU pipeline
        watson_tick = time.perf_counter()
        watson = WatsonNluAnnotator()
        watson_annotations = watson.execute_pipeline(corpus)
        self.pp.pprint(watson_annotations['concepts'])
        watson_tock = time.perf_counter()
        print(f"Identified concepts in {watson_tock - watson_tick:0.4f} seconds")

        # Filter out the similar concepts appearing in both the Spacy and Watson pipelines
        watson_concepts = {term['text'] for term in watson_annotations['concepts']}
        spacy_concepts = {term[0] for term in named_ents}
        similar_concepts = set(watson_concepts).intersection(spacy_concepts)
        self.pp.pprint(similar_concepts)

        # Retrieve relevant triples by concept matching
        query_tick = time.perf_counter()
        triples = []
        for concept in similar_concepts:
            concept = concept.replace(" ", "_")
            result = self.sparql.get_individuals_by_name_with_regex(concept)
            if result == "SPARQL Error!":
                return {
                    'result': None,
                    'status': False,
                    'error': result
                }
            if len(result['results']['bindings']) > 0:
                for individual in result['results']['bindings']:
                    individual_name = individual['individual']['value']
                    individual_result = self.sparql.get_triples_by_subject_with_regex(individual_name)
                    if individual_result == "SPARQL Error!":
                        return {
                            'result': None,
                            'status': False,
                            'error': individual_result
                        }
                    for triple in individual_result['results']['bindings']:
                        triples.append(triple)
        query_tock = time.perf_counter()
        print(f"Queried ontology in {query_tock - query_tick:0.4f} seconds")

        # Generate sentences from retrieved triples
        # TODO Optimize NLG logic
        generated_sentences = []
        nlg_tick = time.perf_counter()

        nlg = NlgEngine()
        nlg_func = partial(nlg.transform)
        with Pool(4) as p:
            gen_sents = p.map(nlg_func, triples)
            generated_sentences = [sent for sent in gen_sents if sent is not None]

        nlg_tock = time.perf_counter()
        print(f"Transformed sentences in {nlg_tock - nlg_tick:0.4f} seconds")

        # Match sentences (generated vs. segmented input) and generate scores for each pair
        # Sentence similarity is scored using 2 metrics using Knowledge-based approach (w/ Wordnet)
        # and Monge-Elkan text distance metric
        similarity_scores = []
        similarity_tick = time.perf_counter()

        me = MongeElkan()
        matcher = SentenceSimilarityMatcher()
        for nlg_sentence in generated_sentences:
            for sentence in sentences:
                tokens_nlg = SpacyNluAnnotator(nlg_sentence).extract_tokens()
                tokens_input = SpacyNluAnnotator(sentence).extract_tokens()
                kb_score = matcher.match_and_fetch_score(nlg_sentence, sentence)
                me_score = me.get_raw_score(tokens_nlg, tokens_input)
                similarity_scores.append({
                    "generated": nlg_sentence,
                    "kb_score": kb_score,
                    "me_score": me_score
                })

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
    # total_tick = time.perf_counter()
    rec = RecommendationsController()
    # pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint(rec.fetch_recommendations("Mercury is the smallest planet in the Solar System. "
    #                                     "It is the first planet from the Sun and is named after a Roman God."))
    # total_tock = time.perf_counter()
    # print(f"Total process in {total_tock - total_tick:0.4f} seconds")

    rec.save_verbalized_recommendations()
