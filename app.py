from flask import Flask, render_template
import os

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])

@app.route("/")
def hello():
    try:
        return "Hi there! This app still in progress, check this out later =D"
    except Exception as e:
	    return ('ERROR ' + str(e))