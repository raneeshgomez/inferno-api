# INFERNO REST API

## Running the app

1. Navigate to the root directory of the project using the terminal
2. Activate the Python 3 virtual environment by running `source .env/bin/activate`
3. Set the FLASK_APP environment variable by running `export FLASK_APP=api.py`
4. Start the Flask API by running `python -m flask run`

## Stopping the app

1. Cause a keyboard interrupt by pressing `Cmd + C` (MacOS) or `Ctrl + C` (Windows\Linux)
2. Additionally, to deactivate the virtual environment, run `deactivate` in terminal

## Running Apache Jena Fuseki SPARQL Server

1. Navigate to the unzipped Fuseki root directory using the terminal
2. Set the JENA_HOME environment variable by running `export JENA_HOME=<absolute path to fuseki directory>`
3. To start the server run, `./fuseki-server --update --mem /ds` in the same terminal
