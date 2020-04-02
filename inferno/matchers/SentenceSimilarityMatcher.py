import nltk
from py_stringmatching import MongeElkan
from pywsd.lesk import simple_lesk
import numpy as np

from inferno.preprocessors.SpacyNluAnnotator import SpacyNluAnnotator


class SentenceSimilarityMatcher:

    def __init__(self):
        print("Initializing INFERNO Knowledge-based Sentence Similarity Matcher...")
        self.me = MongeElkan()

    def compute_string_based_similarity(self, sentence1, sentence2):
        sent1_tokens = SpacyNluAnnotator(sentence1).extract_tokens()
        sent2_tokens = SpacyNluAnnotator(sentence2).extract_tokens()
        return self.me.get_raw_score(sent1_tokens, sent2_tokens)

    def extract_nouns_and_verbs(self, sentence):
        """
            Extracting nouns and verbs for word-based comparison
        """
        # Tokenize sentence
        tokens = nltk.word_tokenize(sentence)
        # Extract POS tags from tokens
        pos_tags = nltk.pos_tag(tokens)
        # Filter tags that are nouns and verbs
        pos_tags = [tag for tag in pos_tags if tag[1].startswith('N') or tag[1].startswith('V')]
        return pos_tags

    def disambiguate_word_senses(self, sentence):
        """
            Disambiguating word senses for nouns and verbs using the LESK algorithm
        """
        # Extract nouns and verbs
        pos_tags = self.extract_nouns_and_verbs(sentence)
        sense = []
        for tag in pos_tags:
            # Fetch correct synset for each tag based on surrounding context
            disambiguated_term = simple_lesk(sentence, tag[0], pos=tag[1][0].lower())
            if disambiguated_term is not None:
                sense.append(disambiguated_term)
        return set(sense)

    def calculate_similarity(self, sense_array_1, sense_array_2, vector_length):
        """
            Generate similarity indexes and vectors
        """
        # Declare list and assign it the length of the synset with the highest number of senses
        # Initialize vector list elements 0.0 by default
        vector = [0.0] * vector_length
        count = 0
        for i, synset_1 in enumerate(sense_array_1):
            similarity_indexes = []
            for synset_2 in sense_array_2:
                # Wu-Palmer similarity is used to calculate the similarity between synsets from each sentence
                # This method is based on the depth of the synsets in the WordNet taxonomy and their common ancestor
                similarity = wn.wup_similarity(synset_1, synset_2)
                if similarity is not None:
                    similarity_indexes.append(similarity)
                else:
                    similarity_indexes.append(0.0)
            # Sort similarity indexes in descending order
            similarity_indexes = sorted(similarity_indexes, reverse=True)
            # Get index with highest similarity
            vector[i] = similarity_indexes[0]
            # Similarity is considered important only if the score is above 0.7
            if vector[i] >= 0.7:
                count += 1
        return vector, count

    def get_shortest_path_distance(self, first_sentence_sense, second_sentence_sense):
        """
            Calculating the shortest path distance for similarity
        """
        if len(first_sentence_sense) >= len(second_sentence_sense):
            vector_length = len(first_sentence_sense)
            v1, c1 = self.calculate_similarity(first_sentence_sense, second_sentence_sense, vector_length)
            v2, c2 = self.calculate_similarity(second_sentence_sense, first_sentence_sense, vector_length)
        if len(second_sentence_sense) > len(first_sentence_sense):
            vector_length = len(second_sentence_sense)
            v1, c1 = self.calculate_similarity(second_sentence_sense, first_sentence_sense, vector_length)
            v2, c2 = self.calculate_similarity(first_sentence_sense, second_sentence_sense, vector_length)
        return np.array(v1), np.array(v2), c1, c2

    def match_and_fetch_score(self, input_sentences, generated_sentences):
        """
            Execute sentence similarity matcher
        """
        similarity_scores = []
        input_sentence_senses = []
        generated_sentence_senses = []
        for input_sentence in input_sentences:
            input_sentence_sense = self.disambiguate_word_senses(input_sentence)
            input_sentence_senses.append({
                'sentence': input_sentence,
                'sense': input_sentence_sense
            })
        for generated_sentence in generated_sentences:
            generated_sentence_sense = self.disambiguate_word_senses(generated_sentence)
            generated_sentence_senses.append({
                'sentence': generated_sentence,
                'sense': generated_sentence_sense
            })

        # Calculate similarity
        for input_sense in input_sentence_senses:
            for generated_sense in generated_sentence_senses:
                # Compute string-based similarity
                string_similarity_score = self.compute_string_based_similarity(input_sense['sentence'],
                                                                               generated_sense['sentence'])
                print("*" * 80)
                print("Monge-Elkan Score for \"" + input_sense['sentence'] + "\" & \"" +
                      generated_sense['sentence'] + "\": " + str(string_similarity_score))

                # Compute knowledge-based similarity
                v1, v2, c1, c2 = self.get_shortest_path_distance(input_sense['sense'], generated_sense['sense'])
                dot_product = np.dot(v1, v2)
                tow = (c1 + c2) / 1.8
                knowledge_based_similarity_score = dot_product / tow
                print("Wu-Palmer Score for \"" + input_sense['sentence'] + "\" & \"" +
                      generated_sense['sentence'] + "\": " + str(knowledge_based_similarity_score))
                print("*" * 80)

                similarity_scores.append({
                    "generated": generated_sense['sentence'],
                    "kb_score": knowledge_based_similarity_score,
                    "me_score": string_similarity_score
                })

        return similarity_scores
