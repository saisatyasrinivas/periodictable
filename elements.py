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
def classification(clss):
    g = rdflib.Graph()
    g.parse("Periodictable.owl")
    print("graph has %s statements." % len(g))

    qres = g.query(
    """
    PREFIX table:<http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    SELECT (?n as ?NAME)
    {{
    ?c table:classification table:{}.
    ?c table:name ?n.
    }}""".format(clss))
    values = []
    for row in qres:
        values.append(row.NAME)
    print(values)
    return jsonify({"options":values})



@app.route('/periodictable/standard_state/<string:state>', methods=['GET'])
def standard_state(state):
    return jsonify({"options":["2"]})


@app.route('/periodictable/block/<string:blk>', methods=['GET'])
def block(blk):
    return jsonify({"options":["1"]})


@app.route('/periodictable/group/<int:gnum>', methods=['GET'])
def group(gnum):
    return jsonify({"options":["1"]})


@app.route('/periodictable/period/<int:pnum>', methods=['GET'])
def period(pnum):
    return jsonify({"options":["1"]})


@app.route('/periodictable/element/<string:sym>', methods=['GET'])
def element(sym):
    g = rdflib.Graph()
    g.parse("Periodictable.owl")
    print("graph has %s statements." % len(g))

    qres = g.query(
    """
    PREFIX table:<http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
    SELECT ?symbol ?atomicNumber ?atomicWeight ?group ?period ?block ?standardState ?color ?classification ?casRegistryID ?group_name
    {{
    ?n   table:name  "{}"^^xsd:string.
    ?n  table:symbol ?symbol.
    ?n  table:atomicNumber ?atomicNumber.
    ?n table:atomicWeight ?atomicWeight.
    ?n table:group       ?group.
    ?n table:period ?period.
    ?n table:block ?block.
    ?n table:standardState ?standardState.
    ?n table:color ?color.
    ?n table:classification ?classification.
    ?n table:casRegistryID ?casRegistryID.
    OPTIONAL {{?group table:name ?group_name.}}
    }}""".format(sym))

    values = {}
    for row in qres:
        values['symbol']= row.symbol
        values['AtomicNumber'] = row.atomicNumber
        values['AtomicWeight'] = row.atomicWeight
        group_name = row.group.split('#')[-1]
        if row.group_name:
            group_name += "({})".format(row.group_name)
        values['GroupName'] = group_name
        values['Period'] = row.period.split('#')[-1]
        values['Block'] = row.block.split('#')[-1]
        values['StandardState'] = row.standardState.split('#')[-1]
        values['color'] = row.color
        values['classification'] = row.classification.split('#')[-1]
        values['casRegistryID'] = row.casRegistryID
    return jsonify({"options":values})



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
