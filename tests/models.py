from mongoengine import *
from datetime import datetime, timezone, timedelta

connect('shortster', host='localhost', port=27017)

class URL(Document):
	original_url = URLField(required=True)
	short_code = StringField(required=True, unique=True)
	timestamp = DateTimeField(default=datetime.now(timezone.utc))
	access_times = StringField()
	unique_id = StringField(required=True)

class ShortURL(Document):
	short_code = StringField(required=True, unique=True)
	used = BooleanField(required=True, default=False)