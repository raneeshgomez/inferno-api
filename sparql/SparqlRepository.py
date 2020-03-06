from sparql.SparqlQueryEngine import SparqlQueryEngine


class SparqlRepository:

    def __init__(self):
        self.sparql = SparqlQueryEngine()

    def get_all_triples(self, limit=1000):
        query = """
            SELECT DISTINCT *
            WHERE {
              ?subject ?predicate ?object .
            }
            LIMIT %s
        """
        query = query % limit
        return self.sparql.query_fuseki(query)

    def get_all_classes(self, limit=1000):
        query = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            
            SELECT DISTINCT ?class
            WHERE {
              ?class a owl:Class.
            }
            LIMIT %s
        """
        query = query % limit
        return self.sparql.query_fuseki(query)

    def get_all_individuals(self, limit=1000):
        query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT DISTINCT ?individual
            WHERE {
              ?individual rdf:type ?type .
              ?type rdfs:subClassOf ?class .
            }
            LIMIT %s
        """
        query = query % limit
        return self.sparql.query_fuseki(query)

    def get_all_properties(self, limit=1000):
        query = """
            SELECT DISTINCT ?property
            WHERE {
              ?subject ?property ?object
            }
            LIMIT %s
        """
        query = query % limit
        return self.sparql.query_fuseki(query)

    def get_individuals_by_name_or_desc_with_regex(self, regex, limit=1000):
        query = """
            PREFIX fss: <http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT DISTINCT ?individual
            WHERE {
              ?individual rdf:type ?type .
              ?type rdfs:subClassOf ?class .
              ?individual fss:description ?description .
              FILTER(regex(str(?individual), "%s") || regex(str(?description), "%s"))
            }
            LIMIT %s
        """
        query = query % (regex, regex, limit)
        return self.sparql.query_fuseki(query)

    def get_description_by_subject(self, subject):
        query = """
            PREFIX fss: <http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#>
    
            SELECT ?object
                WHERE {
                   fss:%s fss:description ?object .
            }
        """
        query = query % subject
        return self.sparql.query_fuseki(query)
