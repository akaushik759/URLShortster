'''
This script retrieves all the URLs which are older than 6 months (180 days) and deletes them one by one from the URL db.
For each deleted URL it updates it status (used = False) in the ShortURL db for reuse
'''

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

#Get 6 month old datetime object for db query
six_month_old_date = datetime.now(timezone.utc) - timedelta(days=180)


try:
	#Retrieve expired URLs
	ExpiredURLs = URL.objects(Q(timestamp__lte=six_month_old_date))
	for each in ExpiredURLs:
		try:
			#Delete each URL from URL db
			res = URL.objects(short_code=each.short_code).delete()
		except Exception as e:
			print("An error :"+str(e)+" occurred while deleting expired URL : \n"+each.short_code+" with _id : "+str(each.id))
		else:
			try:
				#After successful deletion update that short code status for reuse in ShortURL db
				update_status = ShortURL.objects(short_code=each.short_code).update_one(set__used=False, upsert=True)
			except Exception as e:
				print("An error :"+str(e)+" occurred while updating status of short url in ShortURL Db")

except Exception as e:
	print("An error :"+str(e)+" occurred while retreiving expired URLs from URL db")

finally:
	print("Script completed its operation")