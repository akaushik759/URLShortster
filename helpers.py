from .models import *
from .run import redis_client
from datetime import datetime, timezone

import shortuuid
import ast


def isCustomURLAvailable(custom_url):
	try:
		url = ShortURL.objects(short_code=custom_url).first()
		#If not inserted in the short url database then its available
		if not url:
			return True
		#If its inserted into the db but still not used then its available
		if url.used:
			return False
		return True
	except Exception as e:
		print("Error occurred while checking for availability of custom url "+custom_url+" : "+str(e))
		return False

def allotURL(original_url,custom_url=None):
	new_url = None

	#If user has given custom url
	if custom_url:
		unique_id = shortuuid.uuid(name=custom_url)

		#Allot custom url to the original url
		try:
			new_url = URL(original_url=original_url, short_code=custom_url, unique_id=unique_id).save()
		except Exception as e:
			return {'message':'error','error': str(e)}

		#After successful insertion of custom url, update it in the ShortURL db as used(if doesn't exist then insert)
		#If exception occurs in updating the ShortURL db, roll back the changes to URL db and return error
		try:
			mark_status = ShortURL.objects(short_code=custom_url).update_one(set__used=True, upsert=True)
		except Exception as e:
			try:
				delete_url = URL.objects(id=new_url.id).delete()
			except Exception as e:
				return {'message':'error','error': str(e)}
			
			return {'message':'error','error': str(e)}

		return {'message':'success','data': new_url}

	#Get the first unused short url
	unused_short_url = ShortURL.objects(used=False).first()
	unique_id = shortuuid.uuid(name=unused_short_url.short_code)

	#Allot the unused short url to the original url
	try:
		new_url = URL(original_url=original_url, short_code=unused_short_url.short_code, unique_id=unique_id).save()
	except Exception as e:
		return {'message':'error','error': str(e)}

	#After successful insertion of custom url, update it in the ShortURL db as used
	#If exception occurs in updating the ShortURL db, roll back the changes to URL db and return error
	try:
		mark_status = ShortURL.objects(short_code=unused_short_url.short_code).update_one(set__used=True)
	except Exception as e:
		try:
			delete_url = URL.objects(id=new_url.id).delete()
		except Exception as e:
			return {'message':'error','error': str(e)}
			
		return {'message':'error','error': str(e)}

	return {'message':'success','data': new_url}



def fetchOriginalURL(shortcode):
	try:
		cached_url = redis_client.get(shortcode)
		if cached_url:
			return {'message':'success','data': {"original_url":cached_url.decode('utf-8')}}
		original_url = URL.objects(short_code=shortcode).first()
		if original_url:
			access_times = ast.literal_eval(original_url.access_times if original_url.access_times else "[]")
			access_times.append(str(datetime.now(timezone.utc)))
			if len(access_times)>=100:
				redis_client.set(shortcode,str(original_url.original_url).encode('utf-8'))
			try:
				update_stats = URL.objects(short_code=shortcode).update_one(set__access_times=str(access_times))
			except Exception as e:
				print("Error occurred while trying to update the access time of a short url "+shortcode+" : "+str(e))

			return {'message':'success','data': {"original_url":original_url.original_url}}
		return {'message':'error','error':'short url not found in database'}
	except Exception as e:
		return {'message':'error','error':str(e)}
	

def getURLAnalytics(shortcode, unique_id):
	try:
		original_url = URL.objects(short_code=shortcode).first()
		if original_url:
			if original_url.unique_id == unique_id:
				access_times = ast.literal_eval(original_url.access_times if original_url.access_times else "[]")
				last_accessed_time = access_times[-1] if len(access_times) else ""
				count = len(access_times)
				data = {
					'registration_time' : original_url.timestamp,
					'last_accessed_time' : last_accessed_time,
					'count' : count,
					'access_times' : access_times
				}
				return {'message':'success','data':data}
			return {'message':'error','error':'invalid unique id'}
		return {'message':'error','error':'short url not found in database'}

	except Exception as e:
		return {'message':'error','error':str(e)}


def deleteURLData(shortcode, unique_id):
	try:
		original_url = URL.objects(short_code=shortcode).first()
		if original_url:
			if original_url.unique_id == unique_id:
				try:
					delete_original_url = URL.objects(short_code=shortcode).delete()
				except Exception as e:
					return {'message':'error','error':str(e)}

				return {'message':'success','message':'URL was successfully deleted'}
			return {'message':'error','error':'invalid unique id'}
		return {'message':'error','error':'short url not found in database'}
	except Exception as e:
		return {'message':'error','error':str(e)}




