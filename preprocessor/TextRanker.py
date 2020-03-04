import spacy
from collections import OrderedDict
import numpy as np
from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load("en_core_web_sm", disable=['ner'])


# Referred from https://towardsdatascience.com/textrank-for-keyword-extraction-by-python-c0bae21bcec0
class TextRanker:

    def __init__(self, text):
        self.text = text
        self.doc = nlp(self.text)

        # TextRank Configuration
        self.damping_coefficient = 0.85  # damping coefficient, usually is .85
        self.min_diff = 1e-5  # convergence threshold
        self.steps = 10  # iteration steps
        self.node_weight = None  # save keywords and its weight


    def set_custom_stopwords(self, stopwords):
        """Set custom stop words"""
        for word in STOP_WORDS.union(set(stopwords)):
            term = nlp.vocab[word]
            term.is_stop = True

    def segment_sentence(self, candidate_pos, lower):
        """ Store only the words whose type is included in cadidate_pos """
        sentences = []
        for sent in self.doc.sents:
            selected_words = []
            for token in sent:
                # Store words whose POS tag is specified
                if token.pos_ in candidate_pos and token.is_stop is False:
                    if lower is True:
                        selected_words.append(token.text.lower())
                    else:
                        selected_words.append(token.text)
            sentences.append(selected_words)
        return sentences

    def get_vocab(self, sentences):
        """ Add all tokens to an ordered dictionary """
        vocab = OrderedDict()
        i = 0
        for sentence in sentences:
            for word in sentence:
                if word not in vocab:
                    vocab[word] = i
                    i += 1
        return vocab

    def get_token_pairs(self, window_size, sentences):
        """ Build token_pairs from windows in sentences """
        token_pairs = list()
        for sentence in sentences:
            for i, word in enumerate(sentence):
                for j in range(i + 1, i + window_size):
                    if j >= len(sentence):
                        break
                    pair = (word, sentence[j])
                    if pair not in token_pairs:
                        token_pairs.append(pair)
        return token_pairs

    def symmetrize(self, a):
        return a + a.T - np.diag(a.diagonal())

    def get_matrix(self, vocab, token_pairs):
        """ Get normalized matrix """
        # Build matrix
        vocab_size = len(vocab)
        g = np.zeros((vocab_size, vocab_size), dtype='float')
        for word1, word2 in token_pairs:
            i, j = vocab[word1], vocab[word2]
            g[i][j] = 1

        # Get Symmeric matrix
        g = self.symmetrize(g)

        # Normalize matrix by column
        norm = np.sum(g, axis=0)
        g_norm = np.divide(g, norm, where=norm != 0)  # this is ignore the 0 element in norm

        return g_norm

    def get_keywords(self, number=10):
        """ Print top ranking keywords """
        node_weight = OrderedDict(sorted(self.node_weight.items(), key=lambda t: t[1], reverse=True))
        for i, (key, value) in enumerate(node_weight.items()):
            print(key + ' - ' + str(value))
            if i > number:
                break

    def get_all_keywords(self):
        """ Fetch all keywords sorted by rank """
        return OrderedDict(sorted(self.node_weight.items(), key=lambda t: t[1], reverse=True))

    def analyze(self, candidate_pos=['NOUN', 'PROPN'], window_size=4, lower=False, stopwords=list()):
        """ Analyze and preprocess text """

        # Set custom stop words
        self.set_custom_stopwords(stopwords)

        # Filter sentences
        sentences = self.segment_sentence(candidate_pos, lower)  # List of word lists of sentences

        # Build vocabulary
        vocab = self.get_vocab(sentences)

        # Get token_pairs from windows
        token_pairs = self.get_token_pairs(window_size, sentences)

        # Get normalized matrix
        g = self.get_matrix(vocab, token_pairs)

        # Initialization for weight(pagerank value)
        pr = np.array([1] * len(vocab))

        # Iteration
        previous_pr = 0
        for epoch in range(self.steps):
            pr = (1 - self.damping_coefficient) + self.damping_coefficient * np.dot(g, pr)
            if abs(previous_pr - sum(pr)) < self.min_diff:
                break
            else:
                previous_pr = sum(pr)

        # Get weight for each node
        node_weight = dict()
        for word, index in vocab.items():
            node_weight[word] = pr[index]

        self.node_weight = node_weight
