from flask import Flask, render_template
from flask_restful import Resource, Api
import os

app = Flask(__name__)
api = Api(app)

app.config.from_object(os.environ['APP_SETTINGS'])

class Index(Resource):
    def get(self):
        return render_template('index.html')

api.add_resource(Index, '/')