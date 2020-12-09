from flask import jsonify, request
from flask_restful import Resource

#unique shortcode in response
#if chosen shortcode available then allot
#user submitted shortcode to be minimum 4 characters long
#redirect to original url using shortcode
#shortcode has - digits,UC,LC (Case sensitive)
#shortcode can be 6 characters long
#/<shortcode>/stats shows - regd time,last accessed, no. of time accessed

#timeout for URLS?
#handle some urls hit more than the rest

class home(Resource):
	def get(self):
		return jsonify({"message":"hello world"})

	def post(self):
		data = request.get_json()
		return jsonify({"message":"post done"}), 201

class createURL(Resource):
	def post(self):
		data = request.get_json()
		return jsonify({"message":"successfully created URL"})