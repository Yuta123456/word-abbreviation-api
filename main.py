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
@cross_origin(origin=["http://localhost:8100"], supports_credentials=True)
def parse():
    #print(request.get_json())
    data = request.get_json()
    text = data['post_text']

    res = abbreviation(text)
    response = {'result': res}
    #print(response)
    resp = make_response(jsonify(response))
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:8100'
    resp.headers['Access-Control-Allow-Methods'] = 'PUT, ,POST,DELETE, PATCH'
    return resp

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
