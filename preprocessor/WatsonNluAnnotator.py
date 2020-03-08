from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, ConceptsOptions, \
    RelationsOptions, SemanticRolesOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ApiException


class WatsonNluAnnotator:

    def __init__(self):
        authenticator = IAMAuthenticator('VRtIO_wCDZBqX2VyPZvBQKx2qoi3wWm02hpetPPxii77')
        self.service = self.configure_service(authenticator)

    def configure_service(self, authenticator):
        service = NaturalLanguageUnderstandingV1(version='2019-07-12', authenticator=authenticator)
        service.set_service_url(
            'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/dbb2e998'
            '-7cfb-4f67-a74b-0077c7e4faa5')
        return service

    def execute_pipeline(self, corpus):
        try:
            return self.service.analyze(
                text=corpus.resolved_text,
                features=Features(
                    entities=EntitiesOptions(),
                    keywords=KeywordsOptions(),
                    concepts=ConceptsOptions(),
                    relations=RelationsOptions(),
                    semantic_roles=SemanticRolesOptions()
                )
            ).get_result()
        except ApiException as ex:
            return "Method failed with status code " + str(ex.code) + ": " + ex.message