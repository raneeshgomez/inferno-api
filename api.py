from __future__ import unicode_literals, print_function
from flask import Flask, flash, redirect, url_for, session, logging, request, jsonify
from flask_cors import CORS, cross_origin

# Custom imports
from models.corpus import Corpus
from preprocessor.pipeline import NluPipeline

# Base URLs for Spotlight API
annotate_base_url = "http://api.dbpedia-spotlight.org/en/annotate"
candidates_base_url = "http://api.dbpedia-spotlight.org/en/candidates"


HOST = 'localhost'
PORT = 5000

# Creating an instance of the Flask class
# The first argument is the name of the module or package
# This is needed so that Flask knows where to look for templates and static assets
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# *******************************************************************
# Define routes
# *******************************************************************


@app.route('/api', methods=['GET'])
def home():
    return jsonify({"message": "INFERNO API is running on port " + str(PORT)}), 200


@app.route('/api/recommendation', methods=['GET', 'POST'])
@cross_origin()
def generate_recommendations():
    if request.method == 'GET':
        starter_fact = {
            'fact': "This is the starter fact"
        }
        response = jsonify(starter_fact)
        # response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200
    elif request.method == 'POST':
        data = request.json
        text = data['corpus']
        corpus = Corpus(text)

        return "Endpoint under construction", 200
    

if __name__ == '__main__':
    """ 
    Here since the application's module is being run directly, the global(module-level) variable __name__
    is set to the string "__main__".
    But if app.py was to be imported into another module, the __name__ variable would not be equal to
    "__main__", but instead it would be equal to "app" (since the name of this module is app.py).
    Therefore, the if condition here would not be satisfied and the code inside it would not run.
    """
    app.run(host=HOST, port=PORT)
