from flask import jsonify, request
from flask_restful import Resource
from helpers import *

#unique shortcode in response
#if chosen shortcode available then allot
#user submitted shortcode to be minimum 4 characters long
#redirect to original url using shortcode
#shortcode has - digits,UC,LC (Case sensitive)
#shortcode can be 6 characters long
#/<shortcode>/stats shows - regd time,last accessed, no. of time accessed

#timeout for URLS?
#handle some urls hit more than the rest - cache them using redis or memcached
#each api dev key can be limited to certain no. of creations and redirections for time period

#Create URL - original_url, custom_url=None
#Redirect URL - short_url
#Delete URL - unique_key, url_key
#Check Stats - unique_key, short_url


class home(Resource):
	def get(self):
		return jsonify({"message":""})

	def post(self):
		data = request.get_json()
		return jsonify({"message":"post done"}), 201

class createURL(Resource):
	def post(self):
		data = request.get_json()
		original_url = data['original_url']
		if data['custom_url']:
			custom_url = data['custom_url']

			if len(custom_url)<4:
				return jsonify({"message":"an error occurred","error":"short url must be greater than or equal to 4 characters"})

			if isCustomURLAvailable(custom_url):
				result_allot = allotURL(original_url,custom_url)

				if result_allot['message'] == 'success':
					return jsonify({"message":"successfully alloted short custom URL","data":result_allot['data']})						

				return jsonify({"message":"an error occurred","error":result_allot['error']})

			return jsonify({"message":"an error occurred","error":"requested custom url is not available"})

		result_allot = allotURL(original_url)

		if result_allot['message'] = 'success':
			return jsonify({"message":"successfully alloted short URL","data":result_allot['data']})

		return jsonify({"message":"an error occurred","error":result_allot['error']})

class redirectURL(Resource):
	def get(self, shortcode):
		result_fetch = fetchOriginalURL(shortcode)

		if result_fetch['message'] = 'success':
			return jsonify({"message":"successfully found the original url","data":result_fetch['data']})

		return jsonify({"message":"an error occurred","error":result_fetch['error']})

class getAnalytics(Resource):
	def post(self, shortcode):
		data = request.get_json()
		result_fetch = getURLAnalytics(shortcode, data['unique_id'])

		if result_fetch['message'] = 'success':
			return jsonify({"message":"successfully found the url analytics","data":result_fetch['data']})

		return jsonify({"message":"an error occurred","error":result_fetch['error']})

class deleteURL(Resource):
	def post(self, shortcode):
		data = request.get_json()
		result_delete = deleteURL(shortcode, data['unique_id'])

		if result_delete['message'] = 'success':
			return jsonify({"message":"successfully deleted the url"})

		return jsonify({"message":"an error occurred","error":result_delete['error']})






			

