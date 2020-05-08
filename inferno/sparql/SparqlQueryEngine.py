from SPARQLWrapper import SPARQLWrapper, JSON


class SparqlQueryEngine:

    def __init__(self, port=3030, fuseki_endpoint="solar-system"):
        self.PORT = port
        self.FUSEKI_ENDPOINT = fuseki_endpoint
        self.LOCAL_URL = "http://localhost:" + repr(self.PORT) + "/" + self.FUSEKI_ENDPOINT + "/query"
        self.DBPEDIA_URL = "http://dbpedia.org/sparql"

    # Queries Apache Jena Fuseki triple store
    def query_fuseki(self, query):
        sparql = SPARQLWrapper(self.LOCAL_URL)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)

        try:
            ret = sparql.query().convert()
            return ret
        except:
            return "SPARQL Error!"

    # Queries DBpedia
    def query_dbpedia(self, query):
        sparql = SPARQLWrapper(self.DBPEDIA_URL)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)

        try:
            ret = sparql.query().convert()
            return ret
        except:
            return "SPARQL Error!"
