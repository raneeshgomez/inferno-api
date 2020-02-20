import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import math
import re

nlp = spacy.load("en_core_web_lg")


class NluPipeline:

    def __init__(self, text):
        self.text = text
        self.doc = nlp(self.text)
        self.stop_words = set(stopwords.words('english'))

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

    def get_tf_idf_scores_for_text(self):
        sentences = sent_tokenize(self.text)
        cleaned_sentences = [self.strip_special_chars(s) for s in sentences]
        documents = self.get_documents(cleaned_sentences)
        freq_dict_list = self.create_frequency_dictionary(cleaned_sentences)
        tf_scores = self.calculate_tf(documents, freq_dict_list)
        idf_scores = self.calculate_idf(documents, freq_dict_list)
        tf_idf_scores = self.calculate_tf_idf(tf_scores, idf_scores)
        return tf_idf_scores

    def strip_special_chars(self, sentence):
        # Remove special characters
        stripped_sent = re.sub('[^\w\s]', '', sentence)
        stripped_sent = re.sub('_', '', stripped_sent)
        # Replace whitespaces with single space
        stripped_sent = re.sub('\s+', ' ', stripped_sent)
        # Remove whitespaces from start and end
        stripped_sent = stripped_sent.strip()
        return stripped_sent

    def tokenize_and_strip_stop_words(self, sentence):
        # Remove stop words
        word_tokens = word_tokenize(sentence)
        filtered_text = []
        for w in word_tokens:
            if w not in self.stop_words:
                filtered_text.append(w)

        return filtered_text

    def get_documents(self, cleaned_sentences):
        documents = []
        i = 0
        for s in cleaned_sentences:
            i += 1
            count = self.count_words(s)
            doc_obj = {'doc_id': i, 'doc_length': count}
            documents.append(doc_obj)

        return documents

    def count_words(self, sentence):
        words = self.tokenize_and_strip_stop_words(sentence)
        return len(words)

    def create_frequency_dictionary(self, sentences):
        i = 0
        freq_dict_list = []
        for s in sentences:
            i += 1
            freq_dict = {}
            words = self.tokenize_and_strip_stop_words(s)
            for word in words:
                word = word.lower()
                if word in freq_dict:
                    freq_dict[word] += 1
                else:
                    freq_dict[word] = 1
                freq_dict_obj = {'doc_id': i, 'freq_dict': freq_dict}
            freq_dict_list.append(freq_dict_obj)
        return freq_dict_list

    def calculate_tf(self, documents, freq_dict_list):
        tf_scores = []
        for freq_dict in freq_dict_list:
            id = freq_dict['doc_id']
            for dict in freq_dict['freq_dict']:
                tf_score_obj = {
                    'doc_id': id,
                    'tf_score': freq_dict['freq_dict'][dict]/documents[id - 1]['doc_length'],
                    'key': dict
                }
                tf_scores.append(tf_score_obj)
        return tf_scores

    def calculate_idf(self, documents, freq_dict_list):
        idf_scores = []
        count = 0
        for freq_dict in freq_dict_list:
            count += 1
            for dict in freq_dict['freq_dict'].keys():
                count = sum([dict in temp_dict['freq_dict'] for temp_dict in freq_dict_list])
                idf_score_obj = {
                    'doc_id': count,
                    'idf_score': math.log(len(documents)/count),
                    'key': dict
                }
                idf_scores.append(idf_score_obj)
        return idf_scores

    def calculate_tf_idf(self, tf_scores, idf_scores):
        tf_idf_scores = []
        for idf_score in idf_scores:
            for tf_score in tf_scores:
                if idf_score['key'] == tf_score['key'] and idf_score['doc_id'] == tf_score['doc_id']:
                    tf_idf_score_obj = {
                        'doc_id': idf_score['doc_id'],
                        'tf_idf_score': idf_score['idf_score']*tf_score['tf_score'],
                        'key': tf_score['key']
                    }
                    tf_idf_scores.append(tf_idf_score_obj)
        return tf_idf_scores


