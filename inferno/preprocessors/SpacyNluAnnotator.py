import spacy
import neuralcoref

nlp = spacy.load("en")

# Add NeuralCoref into Spacy's annotation pipeline
coref = neuralcoref.NeuralCoref(nlp.vocab)
nlp.add_pipe(coref, name='neuralcoref')


class SpacyNluAnnotator:

    # Extract tokens from text
    def extract_tokens(self, text):
        doc = nlp(text)
        return [token.text for token in doc]

    # Extract lemmas from text
    def extract_lemma(self, text):
        doc = nlp(text)
        return [[token.text, token.lemma_] for token in doc]

    # Extract POS tags from text
    def extract_pos_tags(self, text):
        doc = nlp(text)
        return [[token.text, token.pos_, token.tag_] for token in doc]

    # Extract named entities from text
    def extract_named_ents(self, text):
        doc = nlp(text)
        return [[ent.text, ent.label_] for ent in doc.ents]

    # Extract coreferences from text
    def extract_corefs(self, text):
        doc = nlp(text)
        return doc._.coref_clusters

    # Resolve coreferences in text
    def resolve_corefs(self, text):
        doc = nlp(text)
        return doc._.coref_resolved
