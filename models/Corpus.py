from collections import OrderedDict


class Corpus:

    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.lemmas = []
        self.pos_tags = []
        self.named_entities = []
        self.corefs = []
        self.keywords = OrderedDict()

    def set_annotations(self, tokens, lemmas, pos_tags, named_entities, corefs):
        self.tokens = tokens
        self.lemmas = lemmas
        self.pos_tags = pos_tags
        self.named_entities = named_entities
        self.corefs = corefs

    def fetch_all_linguistic_sets(self):
        return {
            "tokens": self.tokens,
            "lemmas": self.lemmas,
            "pos_tags": self.pos_tags,
            "named_ents": self.named_entities,
            "corefs": self.corefs
        }

    def store_keywords(self, keywords):
        self.keywords = keywords
