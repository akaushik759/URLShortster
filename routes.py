from flask import jsonify, request, make_response, abort
from flask_restful import Resource

from .helpers import *

class createURL(Resource):
	def get(self):
		abort(405)

	def put(self):
		abort(405)

	def delete(self):
		abort(405)

	def post(self):
		if request.headers['Content-Type'] != 'application/json; charset=utf-8':
			return make_response(jsonify({"status":"error","message":"request header needs to be json type"}), 400)
		
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
			return make_response(jsonify({"status":"success","message":"successfully alloted short URL","data":result_allot['data']}), 201)

		return make_response(jsonify({"status":"error","message":result_allot['message']}), 500)

class redirectURL(Resource):
	def post(self, shortcode):
		abort(405)

	def put(self, shortcode):
		abort(405)

	def delete(self, shortcode):
		abort(405)

	def get(self, shortcode):

		if len(shortcode)<4:
			return make_response(jsonify({"status":"error","message":"invalid short url"}), 400)

		result_fetch = fetchOriginalURL(shortcode)

		if result_fetch['status'] == 'success':
			return make_response(jsonify({"status":"success","message":"successfully found the original url","data":result_fetch['data']}), 200)

		if result_fetch['message'] == 'short url not found in database':
			return make_response(jsonify({"status":"error","message":result_fetch['message']}), 200)

		return make_response(jsonify({"status":"error","message":result_fetch['message']}), 500)

class getAnalytics(Resource):
	def post(self, shortcode):
		abort(405)

	def put(self, shortcode):
		abort(405)

	def delete(self, shortcode):
		abort(405)

	def get(self, shortcode):
		try:
			uid = request.headers['unique_id']
		except KeyError:
			return make_response(jsonify({"status":"error","message":"unique id not found in header"}), 400)
		except Exception as e:
			return make_response(jsonify({"status":"error","message":str(e)}), 400)

		if not isinstance(uid, str):
			return make_response(jsonify({"status":"error","message":"unique id needs to be a string"}), 422)

		result_fetch = getURLAnalytics(shortcode, uid)

		if result_fetch['status'] == 'success':
			return make_response(jsonify({"status":"success","message":"successfully found the url analytics","data":result_fetch['data']}), 200)

		if result_fetch['message'] == 'short url not found in database':
			return make_response(jsonify({"status":"error","message":result_fetch['message']}), 200)

		if result_fetch['message'] == 'invalid unique id':
			return make_response(jsonify({"status":"error","message":result_fetch['message']}), 400)

		return make_response(jsonify({"status":"error","message":result_fetch['message']}), 500)

class deleteURL(Resource):
	def get(self, shortcode):
		abort(405)

	def post(self, shortcode):
		abort(405)

	def put(self, shortcode):
		abort(405)

	def delete(self, shortcode):
		try:
			uid = request.headers['unique_id']
		except KeyError:
			return make_response(jsonify({"status":"error","message":"unique id not found in header"}), 400)
		except Exception as e:
			return make_response(jsonify({"status":"error","message":str(e)}), 400)

		if not isinstance(uid, str):
			return make_response(jsonify({"status":"error","message":"unique id needs to be a string"}), 422)

		result_delete = deleteURLData(shortcode, uid)

		if result_delete['status'] == 'success':
			return make_response(jsonify({"status":"success","message":"successfully deleted the url"}), 200)

		if result_delete['message'] == 'short url not found in database':
			return make_response(jsonify({"status":"error","message":result_delete['message']}), 200)

		if result_delete['message'] == 'invalid unique id':
			return make_response(jsonify({"status":"error","message":result_delete['message']}), 400)

		return make_response(jsonify({"status":"error","message":result_delete['message']}), 500)






			

