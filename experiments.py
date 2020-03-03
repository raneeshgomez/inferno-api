from preprocessor.NLUAnnotator import NLUAnnotator
from preprocessor.TextRanker import TextRanker
from preprocessor.TfIdfScorer import TfIdfScorer
from ontologies.SparqlQueryEngine import SparqlQueryEngine
from svo_extractor.subject_verb_object_extract import findSVOs, nlp
from models.Corpus import Corpus
from openie import StanfordOpenIE
from pycorenlp import StanfordCoreNLP
from rake_nltk import Rake
import pke
import requests
import pprint

# DBPedia Resource <http://dbpedia.org/resource/Asturias>
# Fuseki Resource <http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#%s>

# Base URLs for Spotlight API
annotate_base_url = "http://api.dbpedia-spotlight.org/en/annotate"
candidates_base_url = "http://api.dbpedia-spotlight.org/en/candidates"

# ontologies = SparqlQueryEngine()
# query_string = "SELECT * " \
#                "WHERE { " \
#                     "?s <http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#mean_distance_to_sun> ?o. " \
#                     "FILTER (?o < 6)" \
#                "}"
# print(ontologies.query_fuseki(query_string))

corpus = Corpus("Mars is the fourth planet from the Sun and the second-smallest planet in the Solar System, "
                "after Mercury. Named af"
                "ter the Roman god of war, it is often referred to as the 'Red Planet' because "
                "the iron oxide prevalent on its surface gives it a reddish appearance. Mars is a terrestrial planet "
                "with a thin atmosphere, having surface features reminiscent both of the impact craters of the Moon "
                "and the valleys, deserts, and polar ice caps of Earth. The rotational period and seasonal cycles of "
                "Mars are likewise similar to those of Earth, as is the tilt that produces the seasons. Mars is the "
                "site of Olympus Mons, the largest volcano and second-highest known mountain in the Solar System, "
                "and of Valles Marineris, one of the largest canyons in the Solar System. The smooth Borealis basin "
                "in the northern hemisphere covers 40% of the planet and may be a giant impact feature. Mars has two "
                "moons, Phobos and Deimos, which are small and irregularly shaped. These may be captured asteroids, "
                "similar to 5261 Eureka, a Mars trojan. There are ongoing investigations assessing the past "
                "habitability potential of Mars, as well as the possibility of extant life. Future astrobiology "
                "missions are planned, including the Mars 2020 and ExoMars rovers. Liquid water cannot exist on the "
                "surface of Mars due to low atmospheric pressure, which is about  6⁄1000 that of the Earth's, "
                "except at the lowest elevations for short periods. The two polar ice caps appear to be made largely "
                "of water. The volume of water ice in the south polar ice cap, if melted, would be sufficient to "
                "cover the entire planetary surface to a depth of 11 meters (36 ft). Mars can easily be seen from "
                "Earth with the naked eye, as can its reddish coloring. Its apparent magnitude reaches −2.91, "
                "which is surpassed only by Jupiter, Venus, the Moon, and the Sun. Optical ground-based telescopes "
                "are typically limited to resolving features about 300 kilometers (190 mi) across when Earth and Mars "
                "are closest because of Earth's atmosphere.")

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

# Using TF-IDF Scoring

# tf_idf_scorer = TfIdfScorer(corpus.text)
# pp = pprint.PrettyPrinter(indent=2)
# pp.pprint(tf_idf_scorer.get_tf_idf_scores_for_text())

# Using TextRank

sparql_engine = SparqlQueryEngine()
pp = pprint.PrettyPrinter(indent=2)

subject_textranker = TextRanker(corpus.text)
# Analyze corpus with specified candidate POS
subject_textranker.analyze(candidate_pos=['NOUN', 'PROPN'], window_size=4, lower=False)
# Extract keywords using TextRank algorithm
subject_keywords = subject_textranker.get_all_keywords()
pp.pprint(subject_keywords)

predicate_textranker = TextRanker(corpus.text)
# Analyze corpus with specified candidate POS
predicate_textranker.analyze(candidate_pos=['VERB', 'ADJ'], window_size=4, lower=False)
# Extract keywords using TextRank algorithm
predicate_keywords = predicate_textranker.get_all_keywords()
pp.pprint(predicate_keywords)

vo_result_list = []
for i, (key, value) in enumerate(subject_keywords.items()):
    vo_query_string = """
                    PREFIX fss: <http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#>

                    SELECT DISTINCT ?class
                        WHERE {
                           ?class fss:description ?description
                           FILTER(regex(str(?name), "%s") || regex(str(?description), "%s"))
                    }
            """
    vo_query_string = vo_query_string % (key, key)
    query_result = sparql_engine.query_fuseki(vo_query_string)
    if query_result == "SPARQL Error!":
        pp.pprint(query_result)
    vo_result_list.append(query_result)

so_result_list = []
for i, (key, value) in enumerate(predicate_keywords.items()):
    so_query_string = """
                    PREFIX fss: <http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#>

                    SELECT DISTINCT ?class
                        WHERE {
                           ?class fss:description ?description
                           FILTER(regex(str(?description), "%s"))
                    }
            """
    so_query_string = so_query_string % key
    query_result = sparql_engine.query_fuseki(so_query_string)
    if query_result == "SPARQL Error!":
        pp.pprint(query_result)
    so_result_list.append(query_result)

pp.pprint(vo_result_list)
pp.pprint("***********************************************************************************************************")
pp.pprint(so_result_list)


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
# extractor = pke.unsupervised.TopicRank()
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