import requests
import pprint

# Custom imports
from models.Corpus import Corpus
from sparql.SparqlRepository import SparqlRepository
from preprocessor.SpacyNluAnnotator import SpacyNluAnnotator
from preprocessor.TextRanker import TextRanker


class RecommendationController:

    def __init__(self):
        self.sparql = SparqlRepository()
        # Base URLs for DBpedia Spotlight API
        self.spotlight_annotate_base_url = "http://api.dbpedia-spotlight.org/en/annotate"
        self.spotlight_candidates_base_url = "http://api.dbpedia-spotlight.org/en/candidates"
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
        tokens = nlu.extract_tokens()
        lemma = nlu.extract_lemma()
        pos_tags = nlu.extract_pos_tags()
        named_ents = nlu.extract_named_ents()
        corefs = nlu.extract_corefs()
        # Set annotations to corpus
        corpus.set_annotations(tokens, lemma, pos_tags, named_ents, corefs)

        self.pp.pprint(corpus.text)
        self.pp.pprint(named_ents)
        self.pp.pprint(corefs)
        resolved_text = nlu.doc._.coref_resolved
        self.pp.pprint(resolved_text)

        # subject_textranker = TextRanker(corpus.text)
        # # Analyze corpus with specified candidate POS
        # subject_textranker.analyze(candidate_pos=['NOUN', 'PROPN'], window_size=4, lower=False)
        # # Extract keywords using TextRank algorithm
        # subject_keywords = subject_textranker.get_all_keywords()
        # predicate_textranker = TextRanker(corpus.text)
        # # Analyze corpus with specified candidate POS
        # predicate_textranker.analyze(candidate_pos=['VERB', 'ADJ'], window_size=4, lower=False)
        # # Extract keywords using TextRank algorithm
        # predicate_keywords = predicate_textranker.get_all_keywords()
        #
        # vo_result_list = []
        # for i, (key, value) in enumerate(subject_keywords.items()):
        #     query_result = self.sparql.get_individuals_by_name_or_desc_with_regex(key)
        #     if query_result == "SPARQL Error!":
        #         return {
        #             'result': '',
        #             'status': False,
        #             'error': query_result
        #         }
        #     if len(query_result['results']['bindings']) > 0:
        #         vo_result_list.append(query_result['results']['bindings'])
        #
        # so_result_list = []
        # for i, (key, value) in enumerate(predicate_keywords.items()):
        #     query_result = self.sparql.get_individuals_by_name_or_desc_with_regex(key)
        #     if query_result == "SPARQL Error!":
        #         return {
        #             'result': '',
        #             'status': False,
        #             'error': query_result
        #         }
        #     if len(query_result['results']['bindings']) > 0:
        #         so_result_list.append(query_result['results']['bindings'])
        #
        # self.pp.pprint(vo_result_list)
        # self.pp.pprint("**********************************************************************************************")
        # self.pp.pprint(so_result_list)


        # params = {
        #     "text": corpus.text,
        #     "confidence": 0.35
        # }
        # # Response content type
        # headers = {"accept": "application/json"}
        # res = requests.get(self.spotlight_annotate_base_url, params=params, headers=headers)
        # if res.status_code == 200:
        #     result_list = []
        #     non_duplicate_list = {obj['@URI']: obj for obj in res.json()['Resources']}.values()
        #     self.pp.pprint(non_duplicate_list)
        #     for annotation in non_duplicate_list:
        #         vo_query_string = """
        #                 PREFIX dbo: <http://dbpedia.org/ontology/>
        #
        #                 SELECT *
        #                     WHERE {
        #                        <%s> dbo:abstract ?o .
        #                        FILTER (lang(?o) = 'en')
        #                 }
        #         """
        #         vo_query_string = vo_query_string % annotation['@URI']
        #         query_result = self.sparql_engine.query_dbpedia(vo_query_string)
        #         if query_result == "SPARQL Error!":
        #             return {
        #                 'result': '',
        #                 'status': False,
        #                 'error': query_result
        #             }
        #         if len(query_result['results']['bindings']) > 0:
        #             result_list.append(query_result['results']['bindings'][0]['o']['value'])
        #     return {
        #         'result': result_list,
        #         'status': True,
        #         'error': ''
        #     }
        # else:
        #     return {
        #         'result': '',
        #         'status': False,
        #         'error': 'DBpedia Spotlight Error with code ' + str(res.status_code)
        #     }
