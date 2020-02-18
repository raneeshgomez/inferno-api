import spacy

nlp = spacy.load("en_core_web_sm")

# Custom rule-based sentence segmentation strategy
def set_custom_rules(doc):
    for token in doc[:-1]:
        if token.text == "..." or token.text == "|" or token.text == ";":
            doc[token.i + 1].is_sent_start = True
    return doc


nlp.add_pipe(set_custom_rules, before="parser")


class NluPipeline:

    def extract_tokens(self, text):
        doc = nlp(text)
        return [token.text for token in doc]

    def extract_lemma(self, text):
        doc = nlp(text)
        return [[token.text, token.lemma_] for token in doc]

    def extract_pos_tags(self, text):
        doc = nlp(text)
        return [[token.text, token.pos_, token.tag_] for token in doc]

    def extract_syn_dep(self, text):
        doc = nlp(text)
        return [[token.text, token.dep_] for token in doc]

    def extract_is_stop(self, text):
        doc = nlp(text)
        return [[token.text, token.is_stop] for token in doc]

    def extract_named_ents(self, text):
        doc = nlp(text)
        return [[ent.text, ent.label_] for ent in doc.ents]
