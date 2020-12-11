from flask import Flask

from flask_restful import Resource, Api

#Creating flask app
app = Flask(__name__)

#API object
api = Api(app)

from .routes import *

api.add_resource(home,'/')
api.add_resource(createURL,'/create')
api.add_resource(redirectURL,'/<shortcode>')
api.add_resource(getAnalytics,'/<shortcode>/stats')
api.add_resource(deleteURL,'/<shortcode>/delete')


# driver function 
if __name__ == '__main__': 
    app.run() 