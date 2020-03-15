import nltk
from pywsd.lesk import simple_lesk
import numpy as np


class SentenceSimilarityMatcher:

    def __init__(self):
        print("Initializing INFERNO Knowledge-based Sentence Similarity Matcher...")
        self.word_order = False

    def extract_words_to_compare(self, sentence):
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
        pos_tags = self.extract_words_to_compare(sentence)
        sense = []
        for tag in pos_tags:
            # Fetch correct synset for each tag based on surrounding context
            sense.append(simple_lesk(sentence, tag[0], pos=tag[1][0].lower()))
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

    def match_and_fetch_score(self, first_sentence, second_sentence):
        """
            Execute sentence similarity matcher
        """
        first_sentence_sense = self.disambiguate_word_senses(first_sentence)
        second_sentence_sense = self.disambiguate_word_senses(second_sentence)
        filtered_first_sentence_sense = {sense for sense in first_sentence_sense if sense is not None}
        filtered_second_sentence_sense = {sense for sense in second_sentence_sense if sense is not None}
        print("******************************************************************************************************")
        print("Sense for '" + first_sentence + "': " + str(filtered_first_sentence_sense))
        print("Sense for '" + second_sentence + "': " + str(filtered_second_sentence_sense))
        print("******************************************************************************************************")

        v1, v2, c1, c2 = self.get_shortest_path_distance(filtered_first_sentence_sense, filtered_second_sentence_sense)
        print("Vector 01: " + str(v1))
        print("Vector 02: " + str(v2))
        print("Count 01: " + str(c1))
        print("Count 02: " + str(c2))

        dot_product = np.dot(v1, v2)
        tow = (c1 + c2) / 1.8
        final_similarity = dot_product / tow
        # print("Similarity: ", final_similarity)
        return final_similarity


if __name__ == "__main__":
    matcher = SentenceSimilarityMatcher()
    sentence_1 = "An apple a day keeps the doctor away."
    sentence_2 = "An apple a day keeps the doctor away."
    sentence_3 = "Virat Kohli scores century"
    sentence_4 = "Virat Kohli played 100 runs yesterday"
    # print("Similarity: " + str(matcher.match_and_fetch_score(sentence_1, sentence_2)))
    print("Similarity: " + str(matcher.match_and_fetch_score(sentence_3, sentence_4)))
