from __future__ import unicode_literals, print_function

from flask import Flask, flash, redirect, url_for, session, logging, request, jsonify
import spacy

nlp = spacy.load("en_core_web_lg")


# Custom rule-based sentence segmentation strategy
def set_custom_rules(doc):
    for token in doc[:-1]:
        if token.text == "..." or token.text == "|" or token.text == ";":
            doc[token.i + 1].is_sent_start = True
    return doc


nlp.add_pipe(set_custom_rules, before="parser")

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
    text = request.json
    corpus = text['corpus']
    doc = nlp(corpus)
    return jsonify([sent.text for sent in doc.sents]), 200


if __name__ == '__main__':
    """ 
    Here since the application's module is being run directly, the global(module-level) variable __name__
    is set to the string "__main__".
    But if app.py was to be imported into another module, the __name__ variable would not be equal to
    "__main__", but instead it would be equal to "app" (since the name of this module is app.py).
    Therefore, the if condition here would not be satisfied and the code inside it would not run.
    """
    app.run(host=HOST, port=PORT)
