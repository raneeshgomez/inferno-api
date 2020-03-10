from nlglib.realisation.simplenlg.realisation import Realiser
from nlglib.microplanning import *
import math


class NlgEngine:

    def __init__(self):
        self.realise = Realiser(host='nlg.kutlak.info', port=40000)
        self.ontology_base_url = "http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#"
        self.rdf_base_url = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        self.rdfs_base_url = "http://www.w3.org/2000/01/rdf-schema#"
        self.owl_base_url = "http://www.w3.org/2002/07/owl#"

    def transform(self, triple):
        # Remove base URLs from triple
        try:
            ont_subject = self.remove_base_url(triple['subject']['value'])
            ont_predicate = self.remove_base_url(triple['predicate']['value'])
            ont_object = self.remove_base_url(triple['object']['value'])
        except ValueError as ex:
            return ex

        # Remove underscores and add whitespaces to multi-word concepts
        ont_subject = self.add_whitespaces(ont_subject)
        ont_object = self.add_whitespaces(ont_object)

        return self.realise(self.build_sentence(ont_subject, ont_predicate, ont_object))

    def build_sentence(self, ont_subject, ont_predicate, ont_object):
        sentence = Clause()
        if ont_predicate == "isMoonOf":
            sentence = Clause(NP(ont_subject), VP("be"), NP("a moon of", ont_object))
            sentence['TENSE'] = 'PRESENT'
        elif ont_predicate == "subClassOf":
            if ont_subject == "Solar System":
                sentence = Clause(NP("The", ont_subject), VP("be"), NP("our residential system of planets in the", ont_object))
            else:
                sentence = Clause(NP(ont_subject), VP("be"), NP("a", ont_object))
            sentence['TENSE'] = 'PRESENT'
        elif ont_predicate == "circumference":
            if ont_subject == "Sun":
                sentence = Clause(NP("The circumference of the", ont_subject), VP("be"), NP(ont_object))
            else:
                sentence = Clause(NP("The circumference of", ont_subject), VP("be"), NP(ont_object))
            sentence['TENSE'] = 'PRESENT'
        elif ont_predicate == "age":
            temp_age = math.trunc(float(ont_object))
            ont_object = format(temp_age, ",d")
            if ont_subject == "Sun" or ont_subject == "Solar System":
                sentence = Clause(NP("The", ont_subject + "'s", "age"), VP("be"), NP("approximately", ont_object, "years"))
            else:
                sentence = Clause(NP(ont_subject + "'s", "age"), VP("be"), NP("approximately", ont_object, "years"))
            sentence['TENSE'] = 'PRESENT'
        elif ont_predicate == "surface_area":
            if ont_subject == "Sun":
                sentence = Clause(NP("The", ont_subject + "'s", "surface area"), VP("be"), NP(ont_object))
            else:
                sentence = Clause(NP(ont_subject + "'s", "surface area"), VP("be"), NP(ont_object))
            sentence['TENSE'] = 'PRESENT'
        elif ont_predicate == "mean_distance_to_sun":
            sentence = Clause(NP(ont_subject), VP("be"), NP(ont_object + "s", "away from the Sun, where an AU ("
                                                                              "Astronomical Unit) is the distance "
                                                                              "from the Earth to the Sun"))
            sentence['TENSE'] = 'PRESENT'
        elif ont_predicate == "dbpedia_equivalent":
            if ont_subject == "Sun" or ont_subject == "Solar System":
                sentence = Clause(NP("For more information about the", ont_subject, ", please visit"), NP(ont_object))
            else:
                sentence = Clause(NP("For more information about", ont_subject, ", please visit"), NP(ont_object))
            sentence['TENSE'] = 'PRESENT'
        elif ont_predicate == "mass":
            if ont_subject == "Sun":
                sentence = Clause(NP("The", ont_subject + "'s", "mass"), VP("be"), NP(ont_object))
            else:
                sentence = Clause(NP(ont_subject + "'s", "mass"), VP("be"), NP(ont_object))
            sentence['TENSE'] = 'PRESENT'
        elif ont_predicate == "discovered_by":
            if ont_subject == "Sun" or ont_subject == "Solar System":
                sentence = Clause(NP("The", ont_subject), VP("be"), NP("discovered by", ont_object))
            else:
                sentence = Clause(NP(ont_subject), VP("be"), NP("discovered by", ont_object))
            sentence['TENSE'] = 'PAST'
        elif ont_predicate == "discovered_on":
            if ont_subject == "Sun" or ont_subject == "Solar System":
                sentence = Clause(NP("The", ont_subject), VP("be"), NP("discovered in", ont_object))
            else:
                sentence = Clause(NP(ont_subject), VP("be"), NP("discovered in", ont_object))
            sentence['TENSE'] = 'PAST'
        elif ont_predicate == "mean_temperature":
            if ont_subject == "Sun":
                sentence = Clause(NP("The mean temperature on the", ont_subject), VP("be"), NP(ont_object))
            else:
                sentence = Clause(NP("The mean temperature on", ont_subject), VP("be"), NP(ont_object))
            sentence['TENSE'] = 'PRESENT'
        elif ont_predicate == "radius":
            if ont_subject == "Sun":
                sentence = Clause(NP("The radius of the", ont_subject), VP("be"), NP(ont_object))
            else:
                sentence = Clause(NP("The radius of", ont_subject), VP("be"), NP(ont_object))
            sentence['TENSE'] = 'PRESENT'
        elif ont_predicate == "order_from_sun":
            ordinal_generator = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])
            position_ordinal = ordinal_generator(int(ont_object))
            sentence = Clause(NP(ont_subject), VP("be"), NP("the", position_ordinal, "planet from the Sun"))
            sentence['TENSE'] = 'PRESENT'

        return sentence

    def remove_base_url(self, url):
        if self.ontology_base_url in url:
            return url.replace(self.ontology_base_url, "")
        elif self.rdf_base_url in url:
            return url.replace(self.rdf_base_url, "")
        elif self.rdfs_base_url in url:
            return url.replace(self.rdfs_base_url, "")
        elif self.owl_base_url in url:
            return url.replace(self.owl_base_url, "")
        else:
            return url

    def add_whitespaces(self, concept):
        if "_" in concept:
            return concept.replace("_", " ")
        return concept

# nlg = NlgEngine()
# print(nlg.transform(
#     {
#         "subject": {
#             "value": "http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#Mars"
#         },
#         "predicate": {
#             "value": "http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#dbpedia_equivalent"
#         },
#         "object": {
#             "value": "http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#http://dbpedia.org/resource/Mars"
#         },
#     }
# ))