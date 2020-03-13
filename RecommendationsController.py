import pprint
from nltk.tokenize import sent_tokenize
import time
from functools import partial
from multiprocessing.pool import Pool
import math
from py_stringmatching import MongeElkan, Cosine
import operator

# Custom imports
from inference.FuzzyController import FuzzyController
from matchers.SentenceSimilarityMatcher import SentenceSimilarityMatcher
from models.Corpus import Corpus
from nlg.NlgEngine import NlgEngine
from preprocessor.WatsonNluAnnotator import WatsonNluAnnotator
from sparql.SparqlRepository import SparqlRepository
from preprocessor.SpacyNluAnnotator import SpacyNluAnnotator


class RecommendationsController:

    def __init__(self):
        self.sparql = SparqlRepository()
        # Debug logging
        self.pp = pprint.PrettyPrinter(indent=4)

    def fetch_starter_fact(self, domain="Solar System"):
        if domain == "Solar System":
            result = self.sparql.get_description_by_subject("Solar_System")
            if result == "SPARQL Error!":
                return {
                    'result': '',
                    'status': False,
                    'error': result
                }
            return {
                'result': result['results']['bindings'][0]['object']['value'],
                'status': True,
                'error': ''
            }
        else:
            return {
                'result': '',
                'status': False,
                'error': 'Invalid domain'
            }

    def fetch_recommendations(self, text):
        # Initialize new corpus
        corpus = Corpus(text)

        # Annotate corpus for NLU purposes
        nlu = SpacyNluAnnotator(text)
        # Set resolved text to corpus
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
                    'result': '',
                    'status': False,
                    'error': result
                }
            if len(result['results']['bindings']) > 0:
                for individual in result['results']['bindings']:
                    individual_name = individual['individual']['value']
                    individual_result = self.sparql.get_triples_by_subject_with_regex(individual_name)
                    if individual_result == "SPARQL Error!":
                        return {
                            'result': '',
                            'status': False,
                            'error': individual_result
                        }
                    for triple in individual_result['results']['bindings']:
                        triples.append(triple)
        query_tock = time.perf_counter()
        print(f"Queried ontology in {query_tock - query_tick:0.4f} seconds")

        # Generate sentences from retrieved triples
        generated_sentences = []
        nlg_tick = time.perf_counter()
        nlg = NlgEngine()
        for triple in triples:
            if triple['predicate']['value'] != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" and triple['predicate']['value'] != "http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#description":
                sentence = nlg.transform(triple)
                generated_sentences.append(sentence)
        nlg_tock = time.perf_counter()
        print(f"Transformed sentences in {nlg_tock - nlg_tick:0.4f} seconds")

        # Match sentences (generated vs. segmented input) and generate scores for each pair
        similarity_scores = []
        similarity_tick = time.perf_counter()

        # Run sentence similarity using 2 metrics using Knowledge-based approach (w/ Wordnet)
        # and Monge-Elkan text distance metric

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
        fuzzy = FuzzyController()
        fuzzy.initialize_fuzzy_engine()
        fuzzy_scores = []
        for score in similarity_scores:
            score_1 = score['kb_score']
            score_2 = score['me_score']
            if math.isinf(score_1):
                score_1 = 0
            if math.isinf(score_2):
                score_2 = 0
            fuzzy_score = fuzzy.predict_fuzzy_score(score_1, score_2)
            fuzzy_scores.append({
                "sentence": score['generated'],
                "score": fuzzy_score
            })

        # Rank scored sentences in order of relevance
        fuzzy_scores.sort(key=operator.itemgetter('score'), reverse=True)

        return {
            'result': fuzzy_scores,
            'status': True,
            'error': ''
        }


total_tick = time.perf_counter()
rec = RecommendationsController()
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(rec.fetch_recommendations("Mercury is the smallest planet in the Solar System. It is the first planet from the Sun and is named after a Roman God."))
total_tock = time.perf_counter()
print(f"Total process in {total_tock - total_tick:0.4f} seconds")

# Figure out how to optimize this code for multithreading (this is inefficient)
# To use this code, replace it with the inner for loop in sentence similarity section
#
# similarity = partial(matcher.match_and_fetch_score, nlg_sentence)
# with Pool(4) as p:
#     scores = p.map(similarity, sentences)
#     similarity_scores.append({
#         "generated": nlg_sentence,
#         "scores": scores
#     })
