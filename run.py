from flask import Flask

from flask_restful import Resource, Api
from flask_redis import FlaskRedis

#Creating flask app
app = Flask(__name__)

app.config['SECRET_KEY'] = '1@$5323as24d'
app.config['REDIS_URL'] = "redis://localhost:6379/0"

#Redis object
redis_client = FlaskRedis(app)

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