from models import *

def isCustomURLAvailable(custom_url):
	url = ShortURL.objects(short_code=custom_url).first()
	#If not inserted in the short url database then its available
	if not url:
		return True
	#If its inserted into the db but still not used then its available
	if url.used:
		return False
	return True

def allotURL(original_url,custom_url=None):
	pass

def fetchOriginalURL(shortcode):
	pass

def getURLAnalytics(shortcode):
	pass

def deleteURL(shortcode):
	pass