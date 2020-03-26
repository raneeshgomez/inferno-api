from flask_mongoengine import MongoEngine

db = MongoEngine()


# Initialize Mongo database connection
def init_db(app):
    db.init_app(app)
