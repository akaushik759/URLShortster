from mongoengine import *

connect('shortster', host='localhost', port=27017)

class URL(db.Document):
	original_url = db.URLField(required=True)
	short_code = db.StringField(required=True)
	timestamp = db.DateTimeField(default=datetime.datetime.utcnow())
	access_times = db.StringField()
	unique_id = db.StringField(required=True)

reports = Waste.objects((Q(date_time_record__gte=start) & Q(date_time_record__lte=end)))