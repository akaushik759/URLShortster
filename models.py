
from flask_mongoengine import MongoEngine
from .run import app
from datetime import datetime, timezone


app.config['MONGODB_SETTINGS'] = {
    'db': 'shortster',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)

class URL(db.Document):
	original_url = db.URLField(required=True)
	short_code = db.StringField(required=True, unique=True)
	timestamp = db.DateTimeField(default=datetime.now(timezone.utc))
	access_times = db.StringField()
	unique_id = db.StringField(required=True)

class ShortURL(db.Document):
	short_code = db.StringField(required=True, unique=True)
	used = db.BooleanField(required=True, default=False)
