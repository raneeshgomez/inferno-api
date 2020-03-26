from .MongoDb import db


class Recommendation(db.Document):
    semantic_subj = db.StringField(required=True)
    semantic_pred = db.StringField(required=True)
    semantic_obj = db.StringField(required=True)
    recommendation = db.StringField(required=True, unique=True)
    meta = {
        'collection': 'recommendations',
        'indexes': [
            {
                'fields': ['$semantic_subj', '$semantic_obj'],
                'default_language': 'english',
                'weights': {
                    'semantic_subj': 10,
                    'semantic_obj': 7
                }
            }
        ]
    }
