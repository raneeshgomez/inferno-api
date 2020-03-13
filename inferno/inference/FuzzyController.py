import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control


class FuzzyController:

    _relevance_percentage = None

    def __init__(self):
        print("Initializing INFERNO Fuzzy Controller")

    def initialize_fuzzy_engine(self):
        # Declare 2 fuzzy input variables and a fuzzy output variable
        knowledge_based_metric = control.Antecedent(np.arange(0, 1, 0.1), 'Knowledge_Based_Metric')
        text_distance_metric = control.Antecedent(np.arange(0, 1, 0.1), 'Text_Distance_Metric')
        recommendation_relevance = control.Consequent(np.arange(0, 100, 1), 'Recommendation_Relevance')

        # Define membership functions for the sentence similarity antecedent
        knowledge_based_metric['low_relevance'] = fuzzy.trimf(knowledge_based_metric.universe, [0, 0, 0.5])
        knowledge_based_metric['moderate_relevance'] = fuzzy.trimf(knowledge_based_metric.universe, [0, 0.5, 0.9])
        knowledge_based_metric['high_relevance'] = fuzzy.trimf(knowledge_based_metric.universe, [0.5, 0.9, 0.9])

        # Define membership functions for the antecedent
        text_distance_metric['low_relevance'] = fuzzy.trimf(text_distance_metric.universe, [0, 0, 0.5])
        text_distance_metric['moderate_relevance'] = fuzzy.trimf(text_distance_metric.universe, [0, 0.5, 0.9])
        text_distance_metric['high_relevance'] = fuzzy.trimf(text_distance_metric.universe, [0.5, 0.9, 0.9])

        # Define membership functions for the recommendation relevance consequent
        recommendation_relevance['low_relevance'] = fuzzy.trimf(recommendation_relevance.universe, [0, 0, 50])
        recommendation_relevance['moderate_relevance'] = fuzzy.trimf(recommendation_relevance.universe, [0, 50, 99])
        recommendation_relevance['high_relevance'] = fuzzy.trimf(recommendation_relevance.universe, [50, 99, 99])

        # Define rules for the Fuzzy Controller
        rule_1 = control.Rule(knowledge_based_metric['low_relevance'] & text_distance_metric['low_relevance'],
                              recommendation_relevance['low_relevance'])
        rule_2 = control.Rule(knowledge_based_metric['low_relevance'] & text_distance_metric['moderate_relevance'],
                              recommendation_relevance['low_relevance'])
        rule_3 = control.Rule(knowledge_based_metric['low_relevance'] & text_distance_metric['high_relevance'],
                              recommendation_relevance['moderate_relevance'])
        rule_4 = control.Rule(knowledge_based_metric['moderate_relevance'] & text_distance_metric['low_relevance'],
                              recommendation_relevance['low_relevance'])
        rule_5 = control.Rule(knowledge_based_metric['moderate_relevance'] & text_distance_metric['moderate_relevance'],
                              recommendation_relevance['high_relevance'])
        rule_6 = control.Rule(knowledge_based_metric['moderate_relevance'] & text_distance_metric['high_relevance'],
                              recommendation_relevance['high_relevance'])
        rule_7 = control.Rule(knowledge_based_metric['high_relevance'] & text_distance_metric['low_relevance'],
                              recommendation_relevance['moderate_relevance'])
        rule_8 = control.Rule(knowledge_based_metric['high_relevance'] & text_distance_metric['moderate_relevance'],
                              recommendation_relevance['high_relevance'])
        rule_9 = control.Rule(knowledge_based_metric['high_relevance'] & text_distance_metric['high_relevance'],
                              recommendation_relevance['high_relevance'])

        # Define a control system with the defined rule base
        control_system = control.ControlSystem([rule_1, rule_2, rule_3, rule_4, rule_5, rule_6, rule_7, rule_8, rule_9])
        self._relevance_percentage = control.ControlSystemSimulation(control_system)

    def predict_fuzzy_score(self, sentence_similarity, unknown_metric):
        relevance_percentage = self._relevance_percentage
        relevance_percentage.input['Knowledge_Based_Metric'] = sentence_similarity
        relevance_percentage.input['Text_Distance_Metric'] = unknown_metric
        # Calculate the relevance
        relevance_percentage.compute()
        relevance_score = relevance_percentage.output['Recommendation_Relevance']
        return int(round(relevance_score))
