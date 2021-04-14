from flask import Flask, jsonify
from flask_cors import CORS
import rdflib

app = Flask("Periodictable")
app.config["DEBUG"] = True
CORS(app)

g = rdflib.Graph()
g.parse("Periodictable.owl")
print(str(g))

@app.route('/periodictable/standard_states/', methods=['GET'])
def standard_states():
    
    return jsonify({"options":["a","b","c","d"]})

@app.route('/periodictable/classifications/', methods=['GET'])
def classifications():
    return jsonify({"options":["1","2","3","4"]})

@app.route('/periodictable/blocks/', methods=['GET'])
def blocks():
    return jsonify({"options":["HI","IAM","A","STUDENT"]})

@app.route('/periodictable/groups/', methods=['GET'])
def groups():
    return jsonify({"options":["HOW","ARE","YOU","DOING"]})

@app.route('/periodictable/periods/', methods=['GET'])
def periods():
    return jsonify({"options":["I","AM","DOING","GREAT"]})

app.run()