from py_stringmatching import MongeElkan
from pywsd.lesk import simple_lesk

from inferno.preprocessors.SpacyNluAnnotator import SpacyNluAnnotator


class SentenceSimilarityMatcher:

    def __init__(self):
        print("Initializing INFERNO Knowledge-based Sentence Similarity Matcher...")
        self.me = MongeElkan()
        self.spacy = SpacyNluAnnotator()

    def preprocess_sentences(self, sentences):
        """
            Preprocess sentence list
        """
        sentence_senses = []
        for sentence in sentences:
            sentence_sense = self.disambiguate_word_senses(sentence)
            sentence_senses.append({
                'sentence': sentence,
                'sense': sentence_sense
            })
        return sentence_senses

    def extract_nouns_and_verbs(self, sentence):
        """
            Extracting nouns and verbs for word-based comparison
        """
        # Extract POS tags from tokens
        pos_tags = self.spacy.extract_pos_tags(sentence)
        # Filter tags that are nouns and verbs
        pos_tags = [tag for tag in pos_tags if tag[2].startswith('N') or tag[2].startswith('V')]
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
            disambiguated_term = simple_lesk(sentence, tag[0], pos=tag[2][0].lower())
            if disambiguated_term is not None:
                sense.append(disambiguated_term)
        return set(sense)

    def compute_knowledge_based_similarity(self, sense_array_1, sense_array_2):
        """
            Compute knowledge-based similarity for senses using the Wu-Palmer algorithm
        """
        # List of highest sense similarities for 2 sentences
        similarity_vector = []
        for synset_1 in sense_array_1:
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
            similarity_vector.append(similarity_indexes[0])

        average_similarity = sum(similarity_vector)/len(similarity_vector)
        return average_similarity

    def compute_string_based_similarity(self, sentence1, sentence2):
        """
            Compute string-based similarity for sentences using the Monge-Elkan algorithm
        """
        sent1_tokens = self.spacy.extract_tokens(sentence1)
        sent2_tokens = self.spacy.extract_tokens(sentence2)
        return self.me.get_raw_score(sent1_tokens, sent2_tokens)

    def match_and_fetch_score(self, input_sentences, generated_sentences):
        """
            Execute sentence similarity matcher
        """
        similarity_scores = []

        # Preprocess inputs
        input_sentence_senses = self.preprocess_sentences(input_sentences)
        generated_sentence_senses = self.preprocess_sentences(generated_sentences)

        # Calculate similarity
        for generated_sense in generated_sentence_senses:
            for input_sense in input_sentence_senses:
                # Compute string-based similarity
                string_similarity_score = self.compute_string_based_similarity(input_sense['sentence'],
                                                                               generated_sense['sentence'])
                # Compute knowledge-based similarity
                knowledge_based_similarity_score = self.compute_knowledge_based_similarity(input_sense['sense'],
                                                                                           generated_sense['sense'])
                print("*" * 80)
                print("Monge-Elkan Score for \"" + input_sense['sentence'] + "\" & \"" +
                      generated_sense['sentence'] + "\": " + str(string_similarity_score))
                print("Wu-Palmer Score for \"" + input_sense['sentence'] + "\" & \"" +
                      generated_sense['sentence'] + "\": " + str(knowledge_based_similarity_score))
                print("*" * 80)

                similarity_scores.append({
                    "generated": generated_sense['sentence'],
                    "kb_score": knowledge_based_similarity_score,
                    "me_score": string_similarity_score
                })

        return similarity_scores
