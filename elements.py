from flask import Flask, jsonify
from flask_cors import CORS
import rdflib

app = Flask("Periodictable")
app.config["DEBUG"] = True
CORS(app)

g = rdflib.Graph()
g.parse("Periodictable.owl")

@app.route('/periodictable/classifications/', methods=['GET'])
def classifications():
    qres = g.query("""
                  PREFIX table:<http://www.daml.org/2003/01/periodictable/PeriodicTable#>
                  PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                  SELECT (?c as ?options)
                  {
                      ?c rdf:type table:Classification.
                  }
    """)
    values = ['Select a value']
    for row in qres:
        values.append(row.options.split('#')[-1])
    return jsonify({"options":values})

@app.route('/periodictable/standard_states/', methods=['GET'])
def standard_states():
    return jsonify({"options":["a","b","c","d"]})

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