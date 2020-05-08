from inferno.sparql.SparqlQueryEngine import SparqlQueryEngine


class SparqlRepository:

    def __init__(self):
        self.sparql = SparqlQueryEngine()

    # Retrieve all semantic triples from knowledge base
    def get_all_triples(self, limit=1000):
        query = """
            PREFIX fss: <http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT DISTINCT *
            WHERE {
              ?subject ?predicate ?object .
            }
            LIMIT %s
        """
        query = query % limit
        return self.sparql.query_fuseki(query)

    # Retrieve all classes from knowledge base
    def get_all_classes(self, limit=1000):
        query = """
            PREFIX fss: <http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            
            SELECT DISTINCT ?class
            WHERE {
              ?class a owl:Class.
            }
            LIMIT %s
        """
        query = query % limit
        return self.sparql.query_fuseki(query)

    # Retrieve all individuals from knowledge base
    def get_all_individuals(self, limit=1000):
        query = """
            PREFIX fss: <http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#>
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

    # Retrieve all assertions from knowledge base
    def get_all_properties(self, limit=1000):
        query = """
            PREFIX fss: <http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT DISTINCT ?property
            WHERE {
              ?subject ?property ?object
            }
            LIMIT %s
        """
        query = query % limit
        return self.sparql.query_fuseki(query)

    # Retrieve filtered semantic triples by regex from knowledge base
    def get_triples_by_subject_with_regex(self, regex, limit=1000):
        # FILTER(?subject = fss: % s)
        query = """
            PREFIX fss: <http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT DISTINCT ?subject ?predicate ?object
            WHERE {
              ?subject ?predicate ?object .
              FILTER(?subject = <%s>)
            }
            LIMIT %s
        """
        query = query % (regex, limit)
        return self.sparql.query_fuseki(query)

    # Retrieve filtered individuals by regex from knowledge base
    def get_individuals_by_name_with_regex(self, regex, limit=1000):
        query = """
            PREFIX fss: <http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT DISTINCT ?individual
            WHERE {
              ?individual rdf:type ?type .
              ?type rdfs:subClassOf ?class .
              FILTER(regex(str(?individual), "%s"))
            }
            LIMIT %s
        """
        query = query % (regex, limit)
        return self.sparql.query_fuseki(query)

    # Retrieve filtered individuals by name or description from knowledge base
    def get_individuals_by_name_or_desc_with_regex(self, regex, limit=1000):
        query = """
            PREFIX fss: <http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT DISTINCT ?individual
            WHERE {
              ?individual rdf:type ?type .
              ?type rdfs:subClassOf ?class .
              ?individual rdfs:comment ?description .
              FILTER(regex(str(?individual), "%s") || regex(str(?description), "%s"))
            }
            LIMIT %s
        """
        query = query % (regex, regex, limit)
        return self.sparql.query_fuseki(query)

    # Retrieve descriptions by subject from knowledge base
    def get_description_by_subject(self, subject):
        query = """
            PREFIX fss: <http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
            SELECT ?object
                WHERE {
                   fss:%s rdfs:comment ?object .
            }
        """
        query = query % subject
        return self.sparql.query_fuseki(query)
