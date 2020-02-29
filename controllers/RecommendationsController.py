import requests
import pprint

# Custom imports
from ontologies.SparqlQueryEngine import SparqlQueryEngine


class RecommendationController:

    def __init__(self):
        self.sparql_engine = SparqlQueryEngine()
        # Base URLs for DBpedia Spotlight API
        self.spotlight_annotate_base_url = "http://api.dbpedia-spotlight.org/en/annotate"
        self.spotlight_candidates_base_url = "http://api.dbpedia-spotlight.org/en/candidates"
        # Debug logging
        self.pp = pprint.PrettyPrinter(indent=4)

    def fetch_starter_fact(self, domain="Solar System"):
        if domain == "Solar System":
            starter_fact_query = """
                        PREFIX fss: <http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#>
    
                        SELECT *
                            WHERE {
                               fss:Solar_System fss:description ?o .
                        }
                    """
            result = self.sparql_engine.query_fuseki(starter_fact_query)
            if result == "SPARQL Error!":
                return {
                    'result': '',
                    'status': False,
                    'error': result
                }
            return {
                'result': result['results']['bindings'][0]['o']['value'],
                'status': True,
                'error': ''
            }
        else:
            return {
                'result': '',
                'status': False,
                'error': 'Invalid domain'
            }

    def fetch_recommendations(self, corpus):

        # TODO ****************************** Only use last few sentences from corpus ******************************

        params = {
            "text": corpus.text,
            "confidence": 0.35
        }
        # Response content type
        headers = {"accept": "application/json"}
        res = requests.get(self.spotlight_annotate_base_url, params=params, headers=headers)
        if res.status_code == 200:
            result_list = []
            non_duplicate_list = {obj['@URI']: obj for obj in res.json()['Resources']}.values()
            self.pp.pprint(non_duplicate_list)
            for annotation in non_duplicate_list:
                vo_query_string = """
                        PREFIX dbo: <http://dbpedia.org/ontology/>

                        SELECT *
                            WHERE {
                               <%s> dbo:abstract ?o .
                               FILTER (lang(?o) = 'en')
                        }
                """
                vo_query_string = vo_query_string % annotation['@URI']
                query_result = self.sparql_engine.query_dbpedia(vo_query_string)
                if query_result == "SPARQL Error!":
                    return {
                        'result': '',
                        'status': False,
                        'error': query_result
                    }
                if len(query_result['results']['bindings']) > 0:
                    result_list.append(query_result['results']['bindings'][0]['o']['value'])
            return {
                'result': result_list,
                'status': True,
                'error': ''
            }
        else:
            return {
                'result': '',
                'status': False,
                'error': 'DBpedia Spotlight Error with code ' + str(res.status_code)
            }
