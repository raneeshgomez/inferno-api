from SPARQLWrapper import SPARQLWrapper, JSON


class SparqlQueryEngine:

    def __init__(self, port=3030, fuseki_endpoint="solar-system"):
        self.PORT = port
        self.FUSEKI_ENDPOINT = fuseki_endpoint
        self.LOCAL_URL = "http://localhost:" + repr(self.PORT) + "/" + self.FUSEKI_ENDPOINT + "/query"
        self.DBPEDIA_URL = "http://dbpedia.org/sparql"

    def query_fuseki(self, query):
        sparql = SPARQLWrapper(self.LOCAL_URL)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)

        try:
            ret = sparql.query().convert()
            for result in ret:
                print(ret)
            # ret is a stream with the results in XML, see <http://www.w3.org/TR/rdf-sparql-XMLres/>
        except:
            print('SPARQL ERROR!')

    def query_dbpedia(self, query):
        sparql = SPARQLWrapper(self.DBPEDIA_URL)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)

        try:
            ret = sparql.query().convert()
            for result in ret:
                print(ret)
            # ret is a stream with the results in XML, see <http://www.w3.org/TR/rdf-sparql-XMLres/>
        except:
            print('SPARQL ERROR!')

