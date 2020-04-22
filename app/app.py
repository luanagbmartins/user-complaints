from flask import Flask, request, render_template
from services import fetch_prediction as fp

app = Flask(__name__)
@app.route('/')
def index():
      return render_template('index.html')

@app.route('/', methods=['POST'])
def prediction():
      complaint = request.form['complaint']
      name = request.form['name']

      main_product, sub_product = fp.process_text(complaint)

      return render_template('prediction.html', name = name, main_product = main_product, sub_product = sub_product)
