from flask import jsonify, request, make_response, abort
from flask_restful import Resource

from .helpers import *

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
		return make_response(jsonify({"message":"Hua abhi"}), 200)

	def post(self):
		data = request.form
		return make_response(jsonify({"message":"post done"}), 201)

class createURL(Resource):
	def get(self):
		abort(405)

	def put(self):
		abort(405)

	def delete(self):
		abort(405)

	def post(self):
		data = request.get_json()

		if 'original_url' not in data:
			return make_response(jsonify({"status":"error","message":"original url not found in your request"}), 422)
		
		original_url = data['original_url']

		if not isinstance(original_url, str):
			return make_response(jsonify({"status":"error","message":"original url needs to be a string"}), 422)

		if len(original_url) == 0:
			return make_response(jsonify({"status":"error","message":"original url cannot be empty string"}), 422)

		if 'custom_url' in data:
			custom_url = data['custom_url']

			if len(custom_url)<4:
				return make_response(jsonify({"status":"error","message":"short url must be greater than or equal to 4 characters"}), 422)

			if isCustomURLAvailable(custom_url):
				result_allot = allotURL(original_url,custom_url)

				if result_allot['status'] == 'success':
					return make_response(jsonify({"status":"success","message":"successfully alloted short custom URL","data":result_allot['data']}), 201)						

				return make_response(jsonify({"status":"error","message":result_allot['message']}), 500)

			return make_response(jsonify({"status":"error","message":"requested custom url is not available"}), 200)

		result_allot = allotURL(original_url)

		if result_allot['status'] == 'success':
			print(str(result_allot))
			return make_response(jsonify({"status":"success","message":"successfully alloted short URL","data":result_allot['data']}), 201)

		return make_response(jsonify({"status":"error","message":result_allot['message']}), 500)

class redirectURL(Resource):
	def post(self):
		abort(405)

	def put(self):
		abort(405)

	def delete(self):
		abort(405)

	def get(self, shortcode):
		result_fetch = fetchOriginalURL(shortcode)

		if result_fetch['status'] == 'success':
			return make_response(jsonify({"status":"success","message":"successfully found the original url","data":result_fetch['data']}), 200)

		return make_response(jsonify({"status":"error","message":result_fetch['message']}), 500)

class getAnalytics(Resource):
	def post(self):
		abort(405)

	def put(self):
		abort(405)

	def delete(self):
		abort(405)

	def get(self, shortcode):
		try:
			uid = request.headers['unique_id']
		except KeyError:
			return make_response(jsonify({"status":"error","message":"unique id not found in header"}), 500)
		except Exception as e:
			return make_response(jsonify({"status":"error","message":str(e)}), 500)

		result_fetch = getURLAnalytics(shortcode, uid)

		if result_fetch['status'] == 'success':
			return make_response(jsonify({"status":"success","message":"successfully found the url analytics","data":result_fetch['data']}), 200)

		return make_response(jsonify({"status":"error","message":result_fetch['message']}), 500)

class deleteURL(Resource):
	def get(self):
		abort(405)

	def post(self):
		abort(405)

	def put(self):
		abort(405)

	def delete(self, shortcode):
		try:
			uid = request.headers['unique_id']
		except KeyError:
			return make_response(jsonify({"status":"error","message":"unique id not found in header"}), 500)
		except Exception as e:
			return make_response(jsonify({"status":"error","message":str(e)}), 500)

		result_delete = deleteURLData(shortcode, uid)

		if result_delete['status'] == 'success':
			return make_response(jsonify({"status":"success","message":"successfully deleted the url"}), 200)

		return make_response(jsonify({"status":"error","message":result_delete['message']}), 500)






			

