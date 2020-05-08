from nlglib.realisation.simplenlg.realisation import Realiser
from nlglib.microplanning import *
from nlglib.features import NUMBER
import math, pprint


class NlgEngine:

    def __init__(self):
        print("Initializing INFERNO NLG Engine...")
        self.pp = pprint.PrettyPrinter(indent=4)
        self.realise = Realiser(host='nlg.kutlak.info', port=40000)
        self.ontology_base_url = "http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#"
        self.rdf_base_url = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        self.rdfs_base_url = "http://www.w3.org/2000/01/rdf-schema#"
        self.owl_base_url = "http://www.w3.org/2002/07/owl#"
        self.disregarded_types = ['DatatypeProperty', 'ObjectProperty', 'InverseObjectProperty', 'NamedIndividual',
                                  'AnonymousIndividual', 'Class', 'TransitiveProperty', 'FunctionalProperty',
                                  'InverseFunctionalProperty', 'SymmetricProperty', 'Restriction']

    # Main function to begin NLG pipeline
    def transform(self, triples):
        sentence_collection = []

        # Preprocess and format semantic triples
        preprocessed_triples = self.preprocess_and_format_triples(triples)

        for subject_relations in preprocessed_triples:
            sentence_structures_for_subject = self.build_sentences_for_subject(subject_relations)
            if sentence_structures_for_subject:
                for structure in sentence_structures_for_subject:
                    sentence = self.realise(structure['structure'])
                    sentence_collection.append({
                        'semantic_subj': subject_relations['subject'],
                        'semantic_pred': structure['predicate'],
                        'semantic_obj': structure['object'],
                        'recommendation': sentence
                    })

        return sentence_collection

    # Build sentence structure for triple dictionary
    def build_sentences_for_subject(self, triple):
        structures = []
        if triple['subject'][0].isupper():
            ont_subject = triple['subject']
            moons = []
            for relationship in triple['relationships']:
                ont_predicate = relationship['predicate']
                ont_object = relationship['object']
                if ont_predicate == "has_moon":
                    moons.append(ont_object)
                else:
                    # Build sentence structure for extracted subject, predicate and object
                    structure = self.build_sentence(ont_subject, ont_predicate, ont_object)
                    if structure:
                        structures.append({
                            'predicate': ont_predicate,
                            'object': ont_object,
                            'structure': structure
                        })
            # If planet has multiple moons
            if len(moons) > 1:
                moon_string = ", ".join(moons[:-2] + [" and ".join(moons[-2:])])
                sentence = Clause(NP(ont_subject + "'s", "moons", features={NUMBER.plural}), VP("be"), NP(moon_string))
                sentence['TENSE'] = 'PRESENT'
                structures.append({
                    'predicate': 'has_moon',
                    'object': moon_string,
                    'structure': sentence
                })
            # If planet has only a single moon
            elif len(moons) == 1:
                if ont_subject == "Earth":
                    sentence = Clause(NP(ont_subject + "'s", "only natural satellite"), VP("be"), NP("simply called the", moons[0]))
                else:
                    sentence = Clause(NP(ont_subject + "'s", "only natural satellite"), VP("be"), NP(moons[0]))
                sentence['TENSE'] = 'PRESENT'
                structures.append({
                    'predicate': 'has_moon',
                    'object': moons[0],
                    'structure': sentence
                })
        else:
            return None

        return structures

    # Verbalizer rulebase for sentence structure construction
    def build_sentence(self, ont_subject, ont_predicate, ont_object):
        sentence = Clause()
        if ont_predicate == "exist_in":
            sentence = Clause(NP(ont_subject), VP("exist"), NP("in the", ont_object))
            sentence['TENSE'] = 'PRESENT'
        elif ont_predicate == "contains":
            sentence = Clause(NP("The", ont_subject), VP("contain"), NP(ont_object, features={NUMBER.plural}))
            sentence['TENSE'] = 'PRESENT'
        elif ont_predicate == "subClassOf":
            sentence = Clause(NP(ont_subject), VP("be"), NP("a", ont_object, "in the Solar System"))
            sentence['TENSE'] = 'PRESENT'
        elif ont_predicate == "type":
            if ont_object not in self.disregarded_types:
                if ont_object == 'Sun':
                    sentence = Clause(NP("The", ont_subject), VP("is"), NP("the", ont_object, "in the Solar System"))
                else:
                    sentence = Clause(NP(ont_subject), VP("is"), NP("a", ont_object, "in the Solar System"))
            sentence['TENSE'] = 'PRESENT'
        elif ont_predicate == "named_after":
            sentence = Clause(NP(ont_subject), VP("be"), NP("named after", ont_object))
            sentence['TENSE'] = 'PRESENT'
        elif ont_predicate == "also_known_as":
            sentence = Clause(NP(ont_subject), VP("be"), NP("also known as", ont_object))
            sentence['TENSE'] = 'PRESENT'
        elif ont_predicate == "planet_type":
            sentence = Clause(NP(ont_subject), VP("be"), NP("classified as a", ont_object, "planet in the Solar System"))
            sentence['TENSE'] = 'PRESENT'
        elif ont_predicate == "revolution_time":
            sentence = Clause(NP(ont_subject), VP("revolve"), NP("around the Sun in", ont_object))
            sentence['TENSE'] = 'PRESENT'
        elif ont_predicate == "rotation_time":
            if ont_subject == "Sun":
                sentence = Clause(NP("The", ont_subject), VP("rotate"), NP("around its own axis in", ont_object))
            else:
                sentence = Clause(NP(ont_subject), VP("rotate"), NP("around its own axis in", ont_object))
            sentence['TENSE'] = 'PRESENT'
        elif ont_predicate == "circumference":
            if ont_subject == "Sun":
                sentence = Clause(NP("The circumference of the", ont_subject), VP("be"), NP(ont_object))
            else:
                sentence = Clause(NP("The circumference of", ont_subject), VP("be"), NP(ont_object))
            sentence['TENSE'] = 'PRESENT'
        elif ont_predicate == "age":
            if ont_subject == "Sun" or ont_subject == "Solar System":
                sentence = Clause(NP("The", ont_subject + "'s", "age"), VP("be"),
                                  NP("approximately", ont_object))
            else:
                sentence = Clause(NP(ont_subject + "'s", "age"), VP("be"), NP("approximately", ont_object))
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
            ordinal_generator = lambda n: "%d%s" % (
            n, "tsnrhtdd"[(math.floor(n / 10) % 10 != 1) * (n % 10 < 4) * n % 10::4])
            position_ordinal = ordinal_generator(int(ont_object))
            sentence = Clause(NP(ont_subject), VP("be"), NP("the", position_ordinal, "planet from the Sun in our Solar System"))
            sentence['TENSE'] = 'PRESENT'
        else:
            return None

        return sentence

    # Sort and organize semantic triples into custom subject-based data structure
    def preprocess_and_format_triples(self, triples):
        formatted_triples = []
        checked_subjects = []
        for triple in triples:
            checking_subject = triple['subject']['value']
            if checking_subject not in checked_subjects:
                checked_subjects.append(checking_subject)
                # Remove base URLs from subject
                processed_subject = self.remove_base_url(checking_subject)
                # Remove underscores and add whitespaces to multi-word concepts
                processed_subject = self.add_whitespaces(processed_subject)
                relationships_for_single_subject = {
                    'subject': processed_subject,
                    'relationships': []
                }
                for temp in triples:
                    temp_subject = temp['subject']['value']
                    if temp_subject == checking_subject:
                        # Remove base URLs from predicate and object
                        processed_predicate = self.remove_base_url(temp['predicate']['value'])
                        processed_object = self.remove_base_url(temp['object']['value'])
                        # Remove underscores and add whitespaces to multi-word concepts
                        processed_object = self.add_whitespaces(processed_object)
                        relationships_for_single_subject['relationships'].append({
                            'predicate': processed_predicate,
                            'object': processed_object
                        })
                formatted_triples.append(relationships_for_single_subject)
        return formatted_triples

    # Remove base URLs from triple URIs
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

    # Replace underscores with whitespaces for multi-word resources
    def add_whitespaces(self, concept):
        if "_" in concept:
            return concept.replace("_", " ")
        return concept


if __name__ == "__main__":
    nlg = NlgEngine()
    print(nlg.transform(
        {
            "subject": {
                "value": "http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#Mars"
            },
            "predicate": {
                "value": "http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#dbpedia_equivalent"
            },
            "object": {
                "value": "http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#http://dbpedia.org/resource/Mars"
            },
        }
    ))
