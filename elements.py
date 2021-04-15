from flask import Flask, jsonify
from flask_cors import CORS
import rdflib
import os
import threading as td

app = Flask("Periodictable")
app.config["DEBUG"] = True
CORS(app)


@app.route('/periodictable/classifications/', methods=['GET'])
def classifications():
    print('pid:', os.getpid())
    print('thread id:', td.get_ident())
    qres = get_results('Classification')
    values = ['Select a value']
    for row in qres:
        values.append(row.options.split('#')[-1])
    print(values)
    return jsonify({"options":values})

@app.route('/periodictable/standard_states/', methods=['GET'])
def standard_states():
    print('pid:', os.getpid())
    print('thread id:', td.get_ident())
    qres = get_results('StandardState')
    values = ['Select a value']
    for row in qres:
        values.append(row.options.split('#')[-1])
    print(values)
    return jsonify({"options":values})

@app.route('/periodictable/blocks/', methods=['GET'])
def blocks():
    print('pid:', os.getpid())
    print('thread id:', td.get_ident())
    qres = get_results('Block')
    values = ['Select a value']
    for row in qres:
        values.append(row.options.split('#')[-1])
    print(values)
    return jsonify({"options":values})

@app.route('/periodictable/groups/', methods=['GET'])
def groups():
    g = rdflib.Graph()
    g.parse("Periodictable.owl")
    qres = g.query(
    """
    PREFIX table:<http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT (?n as ?NAME)
    { 
    ?c rdf:type table:Group.
    ?c table:number ?n.
    }""")
    values = ['Select a value']
    for row in qres:
        values.append(row.NAME)
    print(values)
    return jsonify({"options":values})

@app.route('/periodictable/periods/', methods=['GET'])
def periods():
    g = rdflib.Graph()
    g.parse("Periodictable.owl")
    qres = g.query(
    """
    PREFIX table:<http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT (?n as ?NAME)
    { 
    ?c rdf:type table:Period.
    ?c table:number ?n.
    }""")
    values = ['Select a value']
    for row in qres:
        values.append(row.NAME)
    print(values)
    return jsonify({"options":values})

@app.route('/periodictable/classification/<string:clss>', methods=['GET'])
def classification():
    return jsonify({"options":["1"]})


@app.route('/periodictable/standard_state/<string:state>', methods=['GET'])
def standard_state():
    return jsonify({"options":["1"]})


@app.route('/periodictable/block/<string:blk>', methods=['GET'])
def block():
    return jsonify({"options":["1"]})


@app.route('/periodictable/group/<int:gnum>', methods=['GET'])
def group():
    return jsonify({"options":["1"]})


@app.route('/periodictable/period/<int:pnum>', methods=['GET'])
def period():
    return jsonify({"options":["1"]})

def get_results(category):
    print("*"*40)
    print(category)
    print("*"*40)
    g = rdflib.Graph()
    g.parse("Periodictable.owl")
    query_string = """
                  PREFIX table:<http://www.daml.org/2003/01/periodictable/PeriodicTable#>
                  PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                  SELECT (?c as ?options)
                  {{
                      ?c rdf:type table:{}.
                  }}
    """.format(category)
    print("*"*40)
    print(query_string)
    print("*"*40)
    qres = g.query(query_string)
    return qres

app.run(threaded=True)
