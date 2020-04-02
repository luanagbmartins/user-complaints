from flask import Flask, request, render_template
from flask_restful import Resource, Api
import os

app = Flask(__name__)
@app.route('/')
def my_form():
      return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
      # prediction, confidence = fp.process_text(complaint)
      prediction = 'Credict card'
      confidence = '0.98'
      name = request.form['name']
      return render_template('prediction.html', name = name, result = prediction, confidence = confidence)
