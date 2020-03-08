import requests
import pprint

# Custom imports
from models.Corpus import Corpus
from preprocessor.WatsonNluAnnotator import WatsonNluAnnotator
from sparql.SparqlRepository import SparqlRepository
from preprocessor.SpacyNluAnnotator import SpacyNluAnnotator
from preprocessor.TextRanker import TextRanker
from nltk.tokenize import sent_tokenize


class RecommendationController:

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
        named_ents = nlu.extract_named_ents()
        corefs = nlu.extract_corefs()

        # Set annotations and resolved text to corpus
        resolved_text = nlu.doc._.coref_resolved
        corpus.set_named_entities(named_ents)
        corpus.set_corefs(corefs)
        corpus.set_resolved_text(resolved_text)

        # Tokenize resolved text into sentences
        sentences = sent_tokenize(resolved_text)
        self.pp.pprint(sentences)

        # Execute Watson NLU pipeline
        watson = WatsonNluAnnotator()
        watson_annotations = watson.execute_pipeline(corpus)
        self.pp.pprint(watson_annotations)

        # Retrieve relevant triples by concept matching
        triples = []
        for concept in watson_annotations['concepts']:
            if concept['relevance'] >= 0.85:
                result = self.sparql.get_individuals_by_name_or_desc_with_regex(concept['text'])
                self.pp.pprint(result)
                if result == "SPARQL Error!":
                    return {
                        'result': '',
                        'status': False,
                        'error': result
                    }
                if len(result['results']['bindings']) > 0:
                    triples.append(result['results']['bindings'])

        # TODO 01 - Transform fetched triples to well-formed sentences
        # TODO 02 - Run new set of sentences through sentence similarity matcher against segmented sentences from input
        # TODO 03 - Find one other metric to score formed sentences against input and execute it
        # TODO 04 - Invoke fuzzy controller and pass scores from (TODO 02) and (TODO 02) and fetch fuzzy relevance score
        # TODO 05 - Rank sentences in descending order based on relevance score and return to client

        return {
            'result': triples,
            'status': True,
            'error': ''
        }
