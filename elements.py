from flask import Flask, jsonify
from flask_cors import CORS

app = Flask("Periodictable")
app.config["DEBUG"] = True
CORS(app)

@app.route('/periodictable/standard_states/', methods=['GET'])
def standard_states():
    return jsonify({"options":["a","b","c","d"]})