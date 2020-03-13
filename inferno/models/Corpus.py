class Corpus:

    def __init__(self, text):
        self.text = text
        self.resolved_text = ''
        self.named_entities = []
        self.corefs = []

    def set_resolved_text(self, resolved_text):
        self.resolved_text = resolved_text

    def set_named_entities(self, named_entities):
        self.named_entities = named_entities

    def set_corefs(self, corefs):
        self.corefs = corefs

    def get_annotations(self):
        return {
            "named_ents": self.named_entities,
            "corefs": self.corefs
        }

    def set_annotations(self, named_entities, corefs):
        self.named_entities = named_entities
        self.corefs = corefs
