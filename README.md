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
2. Allow all permissions by running `chmod -R 777 ./`
3. Set the JENA_HOME environment variable by running `export JENA_HOME=<absolute path to fuseki directory>`
4. To start the server run, `./fuseki-server --update --mem /ds` in the same terminal

### Configuring Fuseki Server for INFERNO

1. Go to http://localhost:3030
2. Navigate to the "manage datasets" tab in the main navigation menu
3. Click the "add new dataset" tab
4. Give the dataset name as "solar-system" and select the dataset type as "In-memory"
5. Click "create dataset"
6. In the "existing datasets" tab, click "upload data" for the newly created dataset
7. Click "select files" and select the RDF file "solar-system.rdf" in `<inferno api directory root>/ontologies/` directory
8. Click "upload now"
