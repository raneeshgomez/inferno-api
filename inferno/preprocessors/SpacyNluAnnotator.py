import spacy
import neuralcoref

nlp = spacy.load("en")

# Add NeuralCoref into Spacy's annotation pipeline
coref = neuralcoref.NeuralCoref(nlp.vocab)
nlp.add_pipe(coref, name='neuralcoref')


class SpacyNluAnnotator:

    def __init__(self, text):
        self.text = text
        self.doc = nlp(self.text)

    def extract_tokens(self):
        return [token.text for token in self.doc]

    def extract_lemma(self):
        return [[token.text, token.lemma_] for token in self.doc]

    def extract_pos_tags(self):
        return [[token.text, token.pos_, token.tag_] for token in self.doc]

    def extract_named_ents(self):
        return [[ent.text, ent.label_] for ent in self.doc.ents]

    def extract_corefs(self):
        return self.doc._.coref_clusters
