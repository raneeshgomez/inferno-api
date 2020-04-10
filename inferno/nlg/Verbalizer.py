import pprint
import time

from inferno.nlg.NlgEngine import NlgEngine
from inferno.sparql.SparqlRepository import SparqlRepository


class Verbalizer:

    def __init__(self):
        self.pp = pprint.PrettyPrinter(indent=4)
        self.pp.pprint("Initializing INFERNO Verbalizer...")
        self.nlg = NlgEngine()
        self.sparql = SparqlRepository()
        self.triples = self.fetch_triples_from_kb()
        print('*' * 80 + ' TRIPLES ' + '*' * 80)
        self.pp.pprint(self.triples['result'])
        print('*' * 100 + ' END TRIPLES ' + '*' * 80)

    def verbalize(self):

        if self.triples['status']:
            self.pp.pprint("Commencing verbalization...")
            nlg_tick = time.perf_counter()

            if self.triples['status']:
                recommendations = self.nlg.transform(self.triples['result'])
            else:
                return self.triples

            nlg_tock = time.perf_counter()
            self.pp.pprint(f"Verbalized ontology in {nlg_tock - nlg_tick:0.4f} seconds")

            return recommendations
        else:
            self.pp.pprint("Verbalization failed!")
            return None

    def fetch_triples_from_kb(self):
        self.pp.pprint("Fetching triples...")
        query_tick = time.perf_counter()

        result = self.sparql.get_all_triples()

        if result == "SPARQL Error!":
            self.pp.pprint("Fetching triples failed due to SPARQL Error!")
            return {
                'result': None,
                'status': False,
                'error': result
            }

        query_tock = time.perf_counter()
        self.pp.pprint(f"Fetched all triples in {query_tock - query_tick:0.4f} seconds")

        if not result['results']['bindings']:
            return {
                'result': None,
                'status': False,
                'error': "No triples found!"
            }

        return {
            'result': result['results']['bindings'],
            'status': True,
            'error': None
        }

if __name__ == "__main__":
    verbalizer = Verbalizer()
    pprint.pprint(verbalizer.verbalize())
