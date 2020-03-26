from __future__ import unicode_literals, print_function
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import time, pprint

# Custom imports
from RecommendationsController import RecommendationsController
from inferno.db.MongoDb import init_db

# Define constants for host and port configuration
HOST = 'localhost'
PORT = 5000

# Creating an instance of the Flask class
# The first argument is the name of the module or package
# This is needed so that Flask knows where to look for templates and static assets
app = Flask(__name__)

# Configure CORS
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Configure database
app.config['MONGODB_SETTINGS'] = {
    'host': 'localhost',
    'port': 27017,
    'db': 'inferno'
}
# Initialize database
init_db(app)

# FOR DEBUG ONLY

# Verbalize ontology
# con = RecommendationsController()
# status = con.save_verbalized_recommendations()
# if status['status']:
#     print(status['result'])
# else:
#     print(status['error'])

# Test fetching recommendations
total_tick = time.perf_counter()
rec = RecommendationsController()
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(rec.fetch_recommendations("Mars is the fourth planet from the Sun and the second-smallest planet in the Solar System, after Mercury. Named after the Roman god of war, it is often referred to as the Red Planet because the iron oxide prevalent on its surface gives it a reddish appearance. Mars is a terrestrial planet with a thin atmosphere, having surface features reminiscent both of the impact craters of the Moon and the valleys, deserts, and polar ice caps of Earth. The rotational period and seasonal cycles of Mars are likewise similar to those of Earth, as is the tilt that produces the seasons. Mars is the site of Olympus Mons, the largest volcano and second-highest known mountain in the Solar System, and of Valles Marineris, one of the largest canyons in the Solar System."))
total_tock = time.perf_counter()
print(f"Total process in {total_tock - total_tick:0.4f} seconds")

# *******************************************************************
# Define routes
# *******************************************************************


@app.route('/api', methods=['GET'])
def home():
    return jsonify({"message": "INFERNO API is running on port " + str(PORT)}), 200


@app.route('/api/recommendation', methods=['GET', 'POST'])
@cross_origin()
def generate_recommendations():
    controller = RecommendationsController()
    if request.method == 'GET':
        result = controller.fetch_starter_fact()
        # If result status is falsy
        if not result['status']:
            # If an invalid composition domain has been specified
            if result['error'] == "Invalid domain":
                response_code = 400
            else:
                # 3rd party API or SPARQL errors
                response_code = 500
        else:
            response_code = 200
        response_data = jsonify(result)
        return response_data, response_code
    elif request.method == 'POST':
        data = request.json
        text = data['corpus']
        total_tick = time.perf_counter()
        result = controller.fetch_recommendations(text)
        total_tock = time.perf_counter()
        print(f"Fetched recommendations in {total_tock - total_tick:0.4f} seconds")
        # If result status is falsy
        if not result['status']:
            # 3rd party API or SPARQL errors
            response_code = 500
        else:
            response_code = 200
        response = jsonify(result)
        return response, response_code


if __name__ == '__main__':
    """ 
    Here since the application's module is being run directly, the global(module-level) variable __name__
    is set to the string "__main__".
    But if app.py was to be imported into another module, the __name__ variable would not be equal to
    "__main__", but instead it would be equal to "app" (since the name of this module is app.py).
    Therefore, the if condition here would not be satisfied and the code inside it would not run.
    """
    app.run(host=HOST, port=PORT, debug=True)
