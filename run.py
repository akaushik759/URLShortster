from flask import Flask
from flask_restful import Resource, Api
from routes import *

#Creating flask app
app = Flask(__name__)

#API object
api = Api(app)


api.add_resource(home,'/')
api.add_resource(createURL,'/create')
api.add_resource(redirectURL,'/redirect')
api.add_resource(getAnalytics,'/<shortcode>/stats')


# driver function 
if __name__ == '__main__': 
  
    app.run(debug = True) 