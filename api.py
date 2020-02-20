from __future__ import unicode_literals, print_function
from flask import Flask, flash, redirect, url_for, session, logging, request, jsonify
from rake_nltk import Rake
import requests

# Custom imports
from models.corpus import Corpus
from preprocessor.pipeline import NluPipeline

r = Rake()

# Base URLs for Spotlight API
annotate_base_url = "http://api.dbpedia-spotlight.org/en/annotate"
candidates_base_url = "http://api.dbpedia-spotlight.org/en/candidates"


HOST = 'localhost'
PORT = 5000

# Creating an instance of the Flask class
# The first argument is the name of the module or package
# This is needed so that Flask knows where to look for templates and static assets
app = Flask(__name__)


# Define routes


@app.route('/py/api', methods=['GET'])
def home():
    return jsonify({"message": "Flask NLU REST API is running"}), 200


@app.route('/py/api/paragraph', methods=['POST'])
def tokenize():
    data = request.json
    text = data['corpus']
    corpus = Corpus(text)

    # Preprocess corpus for NLU
    nlu_pipeline = NluPipeline()
    tokens = nlu_pipeline.extract_tokens(corpus.text)
    lemmas = nlu_pipeline.extract_lemma(corpus.text)
    pos_tags = nlu_pipeline.extract_pos_tags(corpus.text)
    syn_deps = extract_syn_dep(corpus.text)
    is_stops = nlu_pipeline.extract_is_stop(corpus.text)
    named_ents = nlu_pipeline.extract_named_ents(corpus.text)

    # Store NLU preprocess results for corpus
    corpus.store_preprocess_pipeline(tokens, lemmas, pos_tags, syn_deps, is_stops, named_ents)

    # Approach 01 - Using DBpedia Spotlight API to fetch candidates in corpus

    params = {
        "text": corpus.text,
        "confidence": 0.35
    }
    # Response content type
    headers = {"accept": "application/json"}
    res = requests.get(candidates_base_url, params=params, headers=headers)
    if res.status_code != 200:
        # Something went wrong
        return "DBpedia Spotlight Error", res.status_code
    return res.text, 200
    
    # Approach 02 - Using RAKE Algorithm and Spacy to extract keywords and named entities
    #
    # r.extract_keywords_from_text(corpus)
    # ranked_phrases = r.get_ranked_phrases()
    # named_entities = [ent.text for ent in doc.ents]
    # for entity in named_entities:
    #     while entity.casefold() in ranked_phrases:
    #         ranked_phrases.remove(entity.casefold())
    # response_obj = {
    #     "keywords": ranked_phrases,
    #     "entities": named_entities
    # }
    # return jsonify(response_obj), 200

    # Approach 03 - Using Spacy to segment sentences
    #
    # return jsonify([sent.text for sent in doc.sents]), 200
    

if __name__ == '__main__':
    """ 
    Here since the application's module is being run directly, the global(module-level) variable __name__
    is set to the string "__main__".
    But if app.py was to be imported into another module, the __name__ variable would not be equal to
    "__main__", but instead it would be equal to "app" (since the name of this module is app.py).
    Therefore, the if condition here would not be satisfied and the code inside it would not run.
    """
    app.run(host=HOST, port=PORT)
