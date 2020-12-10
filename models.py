from __main__ import app
from flask_mongoengine import MongoEngine

import datetime


app.config['MONGODB_SETTINGS'] = {
    'db': 'your_database',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)

class URL(db.document):
	original_url = db.URLField(required=True)
	short_code = db.StringField(required=True)
	created = db.DateTimeField(default=datetime.datetime.utcnow)
	access_times = db.StringField()
	count = db.IntField(default=0)
	unique_id = db.StringField(required=True)

class ShortURL(db.document):
	short_code = db.StringField(required=True)
	used = db.BooleanField(required=True, default=False)
