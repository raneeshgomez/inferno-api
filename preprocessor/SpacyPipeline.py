import spacy

nlp = spacy.load("en_core_web_lg")


class SpacyPipeline:

    def __init__(self, text):
        self.text = text
        self.doc = nlp(self.text)

    def extract_tokens(self):
        return [token.text for token in self.doc]

    def extract_lemma(self):
        return [[token.text, token.lemma_] for token in self.doc]

    def extract_pos_tags(self):
        return [[token.text, token.pos_, token.tag_] for token in self.doc]

    def extract_is_stop(self):
        return [[token.text, token.is_stop] for token in self.doc]

    def extract_named_ents(self):
        return [[ent.text, ent.label_] for ent in self.doc.ents]
