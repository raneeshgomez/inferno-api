import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control


class FuzzyController:

    _relevance_percentage = None

    def __init__(self):
        print("Initializing INFERNO Fuzzy Controller...")

    def initialize_fuzzy_engine(self):
        # Declare 2 fuzzy input variables and a fuzzy output variable
        knowledge_based_score = control.Antecedent(np.arange(0, 1, 0.1), 'Knowledge_Based_Score')
        string_based_score = control.Antecedent(np.arange(0, 1, 0.1), 'String_Based_Score')
        recommendation_relevance = control.Consequent(np.arange(0, 100, 1), 'Recommendation_Relevance')

        # Define membership functions for the knowledge-based antecedent
        knowledge_based_score['low_relevance'] = fuzzy.trimf(knowledge_based_score.universe, [0, 0, 0.5])
        knowledge_based_score['moderate_relevance'] = fuzzy.trimf(knowledge_based_score.universe, [0, 0.5, 0.9])
        knowledge_based_score['high_relevance'] = fuzzy.trimf(knowledge_based_score.universe, [0.5, 0.9, 0.9])

        # Define membership functions for the string-based antecedent
        string_based_score['low_relevance'] = fuzzy.trimf(string_based_score.universe, [0, 0, 0.5])
        string_based_score['moderate_relevance'] = fuzzy.trimf(string_based_score.universe, [0, 0.5, 0.9])
        string_based_score['high_relevance'] = fuzzy.trimf(string_based_score.universe, [0.5, 0.9, 0.9])

        # Define membership functions for the recommendation relevance consequent
        recommendation_relevance['low_relevance'] = fuzzy.trimf(recommendation_relevance.universe, [0, 0, 50])
        recommendation_relevance['moderate_relevance'] = fuzzy.trimf(recommendation_relevance.universe, [0, 50, 99])
        recommendation_relevance['high_relevance'] = fuzzy.trimf(recommendation_relevance.universe, [50, 99, 99])

        # Define rules for the Fuzzy Controller
        rule_1 = control.Rule(knowledge_based_score['low_relevance'] & string_based_score['low_relevance'],
                              recommendation_relevance['low_relevance'])
        rule_2 = control.Rule(knowledge_based_score['low_relevance'] & string_based_score['moderate_relevance'],
                              recommendation_relevance['low_relevance'])
        rule_3 = control.Rule(knowledge_based_score['low_relevance'] & string_based_score['high_relevance'],
                              recommendation_relevance['moderate_relevance'])
        rule_4 = control.Rule(knowledge_based_score['moderate_relevance'] & string_based_score['low_relevance'],
                              recommendation_relevance['low_relevance'])
        rule_5 = control.Rule(knowledge_based_score['moderate_relevance'] & string_based_score['moderate_relevance'],
                              recommendation_relevance['high_relevance'])
        rule_6 = control.Rule(knowledge_based_score['moderate_relevance'] & string_based_score['high_relevance'],
                              recommendation_relevance['high_relevance'])
        rule_7 = control.Rule(knowledge_based_score['high_relevance'] & string_based_score['low_relevance'],
                              recommendation_relevance['moderate_relevance'])
        rule_8 = control.Rule(knowledge_based_score['high_relevance'] & string_based_score['moderate_relevance'],
                              recommendation_relevance['high_relevance'])
        rule_9 = control.Rule(knowledge_based_score['high_relevance'] & string_based_score['high_relevance'],
                              recommendation_relevance['high_relevance'])

        # Define a control system with the defined rule base
        control_system = control.ControlSystem([rule_1, rule_2, rule_3, rule_4, rule_5, rule_6, rule_7, rule_8, rule_9])
        self._relevance_percentage = control.ControlSystemSimulation(control_system)

    def predict_fuzzy_score(self, knowledge_based_similarity, string_based_similarity):
        relevance_percentage = self._relevance_percentage
        relevance_percentage.input['Knowledge_Based_Score'] = knowledge_based_similarity
        relevance_percentage.input['String_Based_Score'] = string_based_similarity
        # Calculate the relevance
        relevance_percentage.compute()
        relevance_score = relevance_percentage.output['Recommendation_Relevance']
        return int(round(relevance_score))
