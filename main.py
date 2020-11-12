from flask import Flask
from flask import request, make_response, jsonify, render_template
from flask_cors import CORS
from utils import abbreviation
import os
app = Flask(__name__)
CORS(app, support_credentials=True)
@app.route("/", methods=['GET'])
def index():
    return render_template('main.html')

@app.route("/abbreviation", methods=['GET','POST'])

def parse():
    data = request.get_json()
    text = data['post_text']
    res = abbreviation(text)
    response = {'result': res}
    return make_response(jsonify(response))

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
  response.headers.add('Access-Control-Allow-Methods', 'POST')
  return response
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
