# from preprocessors.NLUAnnotator import NLUAnnotator
from inferno.preprocessors.SpacyNluAnnotator import SpacyNluAnnotator
# from sparql.SparqlQueryEngine import SparqlQueryEngine
# from svo_extractor.subject_verb_object_extract import findSVOs, nlp
# from openie import StanfordOpenIE
# from pycorenlp import StanfordCoreNLP
# from rake_nltk import Rake
# import requests

import pprint

# DBPedia Resource <http://dbpedia.org/resource/Asturias>
# Fuseki Resource <http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#%s>

# Base URLs for Spotlight API

annotate_base_url = "http://api.dbpedia-spotlight.org/en/annotate"
candidates_base_url = "http://api.dbpedia-spotlight.org/en/candidates"

# sparql = SparqlQueryEngine()
# query_string = "SELECT * " \
#                "WHERE { " \
#                     "?s <http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#mean_distance_to_sun> ?o. " \
#                     "FILTER (?o < 6)" \
#                "}"
# print(sparql.query_fuseki(query_string))

# corpus = Corpus("Mars is the fourth planet from the Sun and the second-smallest planet in the Solar System"
#                 ". Named after the Roman god of war, it is often referred to as the 'Red Planet' because "
#                 "the iron oxide prevalent on its surface gives it a reddish appearance.")

# Preprocess corpus for NLU

# nlu_pipeline = SpacyPipeline(corpus.text)
# tokens = nlu_pipeline.extract_tokens()
# lemmas = nlu_pipeline.extract_lemma()
# pos_tags = nlu_pipeline.extract_pos_tags()
# syn_deps = nlu_pipeline.extract_syn_dep()
# is_stops = nlu_pipeline.extract_is_stop()
# named_ents = nlu_pipeline.extract_named_ents()

# Store NLU preprocess results for corpus

# corpus.store_preprocess_pipeline(tokens, lemmas, pos_tags, syn_deps, is_stops, named_ents)
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(nlu_pipeline.extract_pos_tags())

# Using SVO Extractor (https://github.com/peter3125/enhanced-subject-verb-object-extraction)

# tokens = nlp(corpus.text)
# svos = findSVOs(tokens)
# print(svos)

# Using Stanford Open IE (https://github.com/philipperemy/Stanford-OpenIE-Python)

# with StanfordOpenIE() as client:
#     for triple in client.annotate(corpus.text):
#         print('|-', triple)

    # graph_image = 'graph.png'
    # client.generate_graphviz_graph(corpus.text, graph_image)
    # print('Graph generated: %s.' % graph_image)

# Using pycorenlp (https://github.com/smilli/py-corenlp) and Stanford CoreNLP
# Requires Stanford CoreNLP Java Server to be running

# nlp = StanfordCoreNLP("http://localhost:9000")
# output = nlp.annotate(corpus.text, properties={
#     'annotators': 'tokenize, pos, ner',
#     'outputFormat': 'json'
# })
# pp = pprint.PrettyPrinter(indent=2)
# pp.pprint(output)


# Using RAKE algorithm

# r = Rake()
# r.extract_keywords_from_text(corpus.text)
# ranked_phrases = r.get_ranked_phrases_with_scores()
# pp = pprint.PrettyPrinter(indent=2)
# pp.pprint(ranked_phrases)


# Using TextRank

# sparql_engine = SparqlQueryEngine()
# pp = pprint.PrettyPrinter(indent=2)
#
# subject_textranker = TextRanker(corpus.text)
# # Analyze corpus with specified candidate POS
# subject_textranker.analyze(candidate_pos=['NOUN', 'PROPN'], window_size=4, lower=False)
# # Extract keywords using TextRank algorithm
# subject_keywords = subject_textranker.get_all_keywords()
# pp.pprint(subject_keywords)
#
# predicate_textranker = TextRanker(corpus.text)
# # Analyze corpus with specified candidate POS
# predicate_textranker.analyze(candidate_pos=['VERB', 'ADJ'], window_size=4, lower=False)
# # Extract keywords using TextRank algorithm
# predicate_keywords = predicate_textranker.get_all_keywords()
# pp.pprint(predicate_keywords)
#
# vo_result_list = []
# for i, (key, value) in enumerate(subject_keywords.items()):
#     vo_query_string = """
#                     PREFIX fss: <http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#>
#
#                     SELECT DISTINCT ?class
#                         WHERE {
#                            ?class fss:description ?description
#                            FILTER(regex(str(?name), "%s") || regex(str(?description), "%s"))
#                     }
#             """
#     vo_query_string = vo_query_string % (key, key)
#     query_result = sparql_engine.query_fuseki(vo_query_string)
#     if query_result == "SPARQL Error!":
#         pp.pprint(query_result)
#     vo_result_list.append(query_result)
#
# so_result_list = []
# for i, (key, value) in enumerate(predicate_keywords.items()):
#     so_query_string = """
#                     PREFIX fss: <http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#>
#
#                     SELECT DISTINCT ?class
#                         WHERE {
#                            ?class fss:description ?description
#                            FILTER(regex(str(?description), "%s"))
#                     }
#             """
#     so_query_string = so_query_string % key
#     query_result = sparql_engine.query_fuseki(so_query_string)
#     if query_result == "SPARQL Error!":
#         pp.pprint(query_result)
#     so_result_list.append(query_result)
#
# pp.pprint(vo_result_list)
# pp.pprint("***********************************************************************************************************")
# pp.pprint(so_result_list)


# Using DBpedia Spotlight API

# engine = SparqlQueryEngine()
# params = {
#         "text": corpus.text,
#         "confidence": 0.35
# }
# Response content type
# headers = {"accept": "application/json"}
# res = requests.get(annotate_base_url, params=params, headers=headers)
# if res.status_code == 200:
#     pp = pprint.PrettyPrinter(indent=4)
#     pp.pprint(res.text)
    # for candidate in res.json()['annotation']['surfaceForm']:
    #     vo_query_string = """
    #             PREFIX dbr: <http://dbpedia.org/resource/>
    #             PREFIX dbo: <http://dbpedia.org/ontology/>
    #
    #             SELECT *
    #                 WHERE {
    #                    dbr:%s dbo:abstract ?o .
    #                    FILTER (lang(?o) = 'en')
    #             }
    #     """
    #     vo_query_string = vo_query_string % candidate['resource']['@uri']
    #     query_result = engine.query_dbpedia(vo_query_string)
    #     pp.pprint(candidate['@name'] + " -> " + candidate['resource']['@uri'])
    #     pp.pprint(query_result)
# else:
    # Something went wrong
    # print("DBpedia Spotlight Error" + str(res.status_code))


# Using PKE (https://github.com/boudinfl/pke)

# # initialize keyphrase extraction model, here TopicRank
# extractor = pke.unsupervised.TextRank()
# # load the content of the document, here document is expected to be in raw
# # format (i.e. a simple text file) and preprocessing is carried out using spacy
# extractor.load_document(input=corpus.text, language='en')
# # keyphrase candidate selection, in the case of TopicRank: sequences of nouns
# # and adjectives (i.e. `(Noun|Adj)*`)
# extractor.candidate_selection()
# # candidate weighting, in the case of TopicRank: using a random walk algorithm
# extractor.candidate_weighting()
# # N-best selection, keyphrases contains the 10 highest scored candidates as
# # (keyphrase, score) tuples
# keyphrases = extractor.get_n_best(n=30)
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(keyphrases)


# Using TfIdfVectorizer in sklearn
#
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.cluster import KMeans
# from sklearn.metrics import adjusted_rand_score
# import numpy
#
# texts = ["This first text talks about houses and dogs",
#         "This is about airplanes and airlines",
#         "This is about dogs and houses too, but also about trees",
#         "Trees and dogs are main characters in this story",
#         "This story is about batman and superman fighting each other",
#         "Nothing better than another story talking about airplanes, airlines and birds",
#         "Superman defeats batman in the last round"]
#
# # vectorization of the texts
# vectorizer = TfidfVectorizer(stop_words="english")
# X = vectorizer.fit_transform(texts)
# # used words (axis in our multi-dimensional space)
# words = vectorizer.get_feature_names()
# print("words", words)
#
#
# n_clusters=3
# number_of_seeds_to_try=10
# max_iter = 300
# number_of_process=2 # seads are distributed
# model = KMeans(n_clusters=n_clusters, max_iter=max_iter, n_init=number_of_seeds_to_try, n_jobs=number_of_process).fit(X)
#
# labels = model.labels_
# # indices of preferible words in each cluster
# ordered_words = model.cluster_centers_.argsort()[:, ::-1]
#
# print("centers:", model.cluster_centers_)
# print("labels", labels)
# print("intertia:", model.inertia_)
#
# texts_per_cluster = numpy.zeros(n_clusters)
# for i_cluster in range(n_clusters):
#     for label in labels:
#         if label==i_cluster:
#             texts_per_cluster[i_cluster] +=1
#
# print("Top words per cluster:")
# for i_cluster in range(n_clusters):
#     print("Cluster:", i_cluster, "texts:", int(texts_per_cluster[i_cluster])),
#     for term in ordered_words[i_cluster, :10]:
#         print("\t"+words[term])
#
# print("\n")
# print("Prediction")
#
# text_to_predict = "Why batman was defeated  by superman so easy?"
# Y = vectorizer.transform([text_to_predict])
# predicted_cluster = model.predict(Y)[0]
# texts_per_cluster[predicted_cluster]+=1
#
# print(text_to_predict)
# print("Cluster:", predicted_cluster, "texts:", int(texts_per_cluster[predicted_cluster])),
# for term in ordered_words[predicted_cluster, :10]:
#     print("\t"+words[term])


# From RecommendationController.py

# subject_textranker = TextRanker(corpus.text)
# # Analyze corpus with specified candidate POS
# subject_textranker.analyze(candidate_pos=['NOUN', 'PROPN'], window_size=4, lower=False)
# # Extract keywords using TextRank algorithm
# subject_keywords = subject_textranker.get_all_keywords()
# predicate_textranker = TextRanker(corpus.text)
# # Analyze corpus with specified candidate POS
# predicate_textranker.analyze(candidate_pos=['VERB', 'ADJ'], window_size=4, lower=False)
# # Extract keywords using TextRank algorithm
# predicate_keywords = predicate_textranker.get_all_keywords()
#
# vo_result_list = []
# for i, (key, value) in enumerate(subject_keywords.items()):
#     query_result = self.sparql.get_individuals_by_name_or_desc_with_regex(key)
#     if query_result == "SPARQL Error!":
#         return {
#             'result': '',
#             'status': False,
#             'error': query_result
#         }
#     if len(query_result['results']['bindings']) > 0:
#         vo_result_list.append(query_result['results']['bindings'])
#
# so_result_list = []
# for i, (key, value) in enumerate(predicate_keywords.items()):
#     query_result = self.sparql.get_individuals_by_name_or_desc_with_regex(key)
#     if query_result == "SPARQL Error!":
#         return {
#             'result': '',
#             'status': False,
#             'error': query_result
#         }
#     if len(query_result['results']['bindings']) > 0:
#         so_result_list.append(query_result['results']['bindings'])
#
# self.pp.pprint(vo_result_list)
# self.pp.pprint("**********************************************************************************************")
# self.pp.pprint(so_result_list)



# params = {
#     "text": corpus.text,
#     "confidence": 0.35
# }
# # Response content type
# headers = {"accept": "application/json"}
# res = requests.get(self.spotlight_annotate_base_url, params=params, headers=headers)
# if res.status_code == 200:
#     result_list = []
#     non_duplicate_list = {obj['@URI']: obj for obj in res.json()['Resources']}.values()
#     self.pp.pprint(non_duplicate_list)
#     for annotation in non_duplicate_list:
#         vo_query_string = """
#                 PREFIX dbo: <http://dbpedia.org/ontology/>
#
#                 SELECT *
#                     WHERE {
#                        <%s> dbo:abstract ?o .
#                        FILTER (lang(?o) = 'en')
#                 }
#         """
#         vo_query_string = vo_query_string % annotation['@URI']
#         query_result = self.sparql_engine.query_dbpedia(vo_query_string)
#         if query_result == "SPARQL Error!":
#             return {
#                 'result': '',
#                 'status': False,
#                 'error': query_result
#             }
#         if len(query_result['results']['bindings']) > 0:
#             result_list.append(query_result['results']['bindings'][0]['o']['value'])
#     return {
#         'result': result_list,
#         'status': True,
#         'error': ''
#     }
# else:
#     return {
#         'result': '',
#         'status': False,
#         'error': 'DBpedia Spotlight Error with code ' + str(res.status_code)
#     }

# from py_stringmatching import MongeElkan
#
# me = MongeElkan()
# spacy_1 = SpacyNluAnnotator("Mercury is the smallest planet in the Solar System and is the first planet from the Sun")
# spacy_2 = SpacyNluAnnotator("My name is Khan")
# tokens_1 = spacy_1.extract_tokens()
# tokens_2 = spacy_2.extract_tokens()
# print(me.get_raw_score(tokens_1, tokens_2))

# me_sim = textdistance.hamming.similarity("Mercury",
#                                             "Mercury")
# me_dis = textdistance.hamming.distance("Mercury is the smallest planet in the Solar System and is the first planet from the Sun",
#                                             "Mercury is the smallest planet in the Solar System and is the first planet from the Sun")

# Mercury is the smallest planet in the Solar System and is the first planet from the Sun
#Mercury is 0.387 AUs away from the Sun, where an AU (Astronomical Unit) is the distance from the Earth to the Sun.
# print(me_sim)
# print(me_dis)

import logging

from nlglib.realisation.simplenlg.realisation import Realiser
from nlglib.lexicalisation import Lexicaliser
from nlglib.macroplanning import *
from nlglib.microplanning import *
from nlglib.features import TENSE, ASPECT, NUMBER

realise = Realiser(host='nlg.kutlak.info')


def main():
    c = Clause('Mary', 'chase', 'the monkey')
    print(realise(c))
    tense()
    negation()
    interrogative()
    complements()
    modifiers()
    coordinations()
    prepositional_phrase()
    coordinated_clause()
    subordinate_clause()


def tense():
    c = Clause('Mary', 'chase', 'the monkey')
    c['TENSE'] = 'PAST'
    print(realise(c))
    c['TENSE'] = 'FUTURE'
    print(realise(c))


def negation():
    c = Clause('Mary', 'chase', 'the monkey')
    c['NEGATED'] = 'true'
    print(realise(c))


def interrogative():
    c = Clause('Mary', 'chase', 'the monkey')
    c['INTERROGATIVE_TYPE'] = 'YES_NO'
    print(realise(c))
    c['INTERROGATIVE_TYPE'] = 'WHO_OBJECT'
    print(realise(c))


def complements():
    c = Clause('Mary', 'chase', 'the monkey',
               complements=['very quickly', 'despite her exhaustion'])
    print(realise(c))


def modifiers():
    subject = NP('Mary')
    verb = VP('chase')
    objekt = NP('the', 'monkey')
    subject += Adjective('fast')
    c = Clause()
    c.subject = subject
    c.predicate = verb
    c.object = objekt
    print(realise(c))
    verb += Adverb('quickly')
    c = Clause(subject, verb, objekt)
    print(realise(c))


def coordinations():
    subject1 = NP('Mary')
    subject2 = NP('your', 'giraffe')  # BUG
    subj1 = Coordination(subject1, subject2)
    subj2 = CC(subject1, subject2)
    assert subj1 == subj2
    c = Clause(subj1, VP('chase'), NP('the', 'monkey'))
    print(realise(c))
    subject1 = NP('Mary')
    subject2 = NP('your giraffe')
    subj = subject1 + subject2
    obj = NP('the monkey') + NP('George')
    obj += NP('Martha')
    c = Clause(subj, VP('chase'), obj)
    print(realise(c))
    obj.conj = 'or'
    print(realise(c))


def prepositional_phrase():
    c = Clause('Mary', 'chase', 'the monkey')
    c.complements += PP('in', 'the park')
    print(realise(c))
    c = Clause('Mary', 'chase', 'the monkey')
    c.complements += PP('in', NP('the', 'park'))
    print(realise(c))


def coordinated_clause():
    s1 = Clause('my cat', 'like', 'fish', features={'TENSE': 'PAST'})
    s2 = Clause('my dog', 'like', 'big bones', features={'TENSE': 'PRESENT'})
    s3 = Clause('my horse', 'like', 'grass', features={'TENSE': 'FUTURE'})
    c = s1 + s2 + s3
    c = CC(s1, s2, s3)
    print(realise(s1))
    print(realise(s2))
    print(realise(s3))
    print(realise(s1 + s2))
    print(realise(c))


def subordinate_clause():
    p = Clause('I', 'be', 'happy')
    q = Clause('I', 'eat', 'fish')
    q['COMPLEMENTISER'] = 'because'
    q['TENSE'] = 'PAST'
    p.complements += q
    print(realise(p))

def run():

    realise = Realiser(host='nlg.kutlak.info')
    lex = Lexicaliser(templates={
        'x': String('X'),
        'arthur': Male('Arthur'),
        'shrubbery': Clause(Var(0), VP('find', NP('a', 'shrubbery'), features=[TENSE.future])),
        'knight': Clause(Var(0), VP('is', NP('a', 'knight'))),
        'say_ni': Clause(Var(0), VP('say', Interjection('"Ni!"'))),
    })
    print(realise(lex(formula_to_rst(expr(r'x')))))
    print(realise(lex(formula_to_rst(expr(r'-x')))))

    print(realise(lex(formula_to_rst(expr(r'x = 5')))))
    print(realise(lex(formula_to_rst(expr(r'x != 5')))))

    print(realise(lex(formula_to_rst(expr(r'knight(arthur)')))))
    print(realise(lex(formula_to_rst(expr(r'-knight(arthur)')))))
    print(realise(lex(formula_to_rst(expr(r'say_ni(arthur)')))))
    print(realise(lex(formula_to_rst(expr(r'-say_ni(arthur)')))))
    print(realise(lex(formula_to_rst(expr(r'shrubbery(arthur)')))))
    print(realise(lex(formula_to_rst(expr(r'-shrubbery(arthur)')))))

    print(realise(lex(formula_to_rst(expr(r'knight(arthur) & say_ni(arthur)')))))
    print(realise(lex(formula_to_rst(expr(r'say_ni(arthur) | knight(arthur)')))))
    print(realise(lex(formula_to_rst(expr(r'say_ni(arthur) -> knight(arthur)')))))
    print(realise(lex(formula_to_rst(expr(r'knight(arthur) <-> say_ni(arthur)')))))

    print(realise(lex(formula_to_rst(expr(r'say_ni(arthur) & -knight(arthur)')))))
    print(realise(lex(formula_to_rst(expr(r'say_ni(arthur) | -knight(arthur)')))))
    print(realise(lex(formula_to_rst(expr(r'say_ni(arthur) -> -knight(arthur)')))))
    print(realise(lex(formula_to_rst(expr(r'-knight(arthur) <-> say_ni(arthur)')))))
    print(realise(lex(formula_to_rst(expr(r'-knight(arthur) <-> -say_ni(arthur)')))))
    print(realise(lex(formula_to_rst(expr(r'-(knight(arthur) <-> say_ni(arthur))')))))

    print(realise(lex(formula_to_rst(expr(r'say_ni(arthur) & knight(arthur) & shrubbery(arthur)')))))
    print(realise(lex(formula_to_rst(expr(r'say_ni(arthur) | knight(arthur) | shrubbery(arthur)')))))

def run_simple_examples():
    s = String('This is my string')
    print(realise(s))

    s = Clause(NNP('John'), VP('be', AdjP('happy')))
    print(realise(s))

    s = Clause(NNP('Paul'), VP('play', NP('guitar'), features={ASPECT.progressive, }))
    print(realise(s))

    guitarists = Coordination(Clause(NNP('John'),
                                     VP('play', NP('a', 'guitar'),
                                        features={ASPECT.progressive, TENSE.past, })),
                              Clause(NNP('George'),
                                     VP('play', NP('a', 'guitar'),
                                        features={ASPECT.progressive, TENSE.past, })),
                              Clause(NNP('Paul'),
                                     VP('play', NP('a', 'guitar'),
                                        features={ASPECT.progressive, TENSE.past, }))
                              )
    print(realise(guitarists))

    gringo = Coordination(Clause(NNP('George'),
                                 VP('play', NP('a', 'bass'),
                                    features={ASPECT.progressive, TENSE.past, })),
                          Clause(NNP('Ringo'),
                                 VP('play', NP('drum', features={NUMBER.plural, }),
                                    features={ASPECT.progressive, TENSE.past, }))
                          )
    print(realise(gringo))

def run_pipeline():
    templates = {
        'john': NNP(Male('John')),
        'paul': NNP(Male('Paul')),
        'george': NNP(Male('George')),
        'ringo': NNP(Male('Ringo')),
        'guitar': Noun('guitar'),
        'bass': Noun('bass guitar'),
        'drums': Noun('drum', features={NUMBER.plural, }),
        'Happy': Clause(NP(Var(0)), VP('be', AdjP('happy'))),
        'Play': Clause(NP(Var(0)), VP('play', NP(Var(1)))),
    }

    lex = Lexicaliser(templates=templates)
    # FIXME: embedded coordination doesn't work; flatten or fix in simplenlg?
    input_str = 'Play(john, guitar) & Play(paul, guitar) & ' \
                'Play(george, bass) & Play(ringo, drums)'
    sentence = lex(formula_to_rst(expr(input_str)))
    for e in sentence.elements():
        print(repr(e))

    output_str = realise(sentence)
    print(output_str)


sentence = "Mars is the fourth planet from the Sun and the second-smallest planet in the Solar System, after Mercury."

# Tokenize sentence
tokens = nltk.word_tokenize(sentence)
# Extract POS tags from tokens
pos_tags = nltk.pos_tag(tokens)
print(str(pos_tags))

spacy = SpacyNluAnnotator()
tokens = spacy.extract_tokens(sentence)
pos_tags = spacy.extract_pos_tags(sentence)
print(str(pos_tags))

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    # main()
    # run()
    # run_simple_examples()
    # run_pipeline()