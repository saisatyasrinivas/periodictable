from flask import Flask, jsonify, request
from flask_cors import CORS
import rdflib
import os
import threading as td

app = Flask("Periodictable")
app.config["DEBUG"] = True
CORS(app)


@app.route('/periodictable/classifications/', methods=['GET'])
def classifications():
    qres = get_results('Classification')
    values = ['Select a value']
    for row in qres:
        values.append(row.options.split('#')[-1])
    return jsonify({"options":values})

@app.route('/periodictable/standard_states/', methods=['GET'])
def standard_states():
    qres = get_results('StandardState')
    values = ['Select a value']
    for row in qres:
        values.append(row.options.split('#')[-1])
    return jsonify({"options":values})

@app.route('/periodictable/blocks/', methods=['GET'])
def blocks():
    qres = get_results('Block')
    values = ['Select a value']
    for row in qres:
        values.append(row.options.split('#')[-1])
    return jsonify({"options":values})

@app.route('/periodictable/groups/', methods=['GET'])
def groups():
    g = rdflib.Graph()
    g.parse("Periodictable.owl")
    qres = g.query(
    """
    PREFIX table:<http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT (?n as ?NAME) ?group_name
    { 
    ?c rdf:type table:Group.
    ?c table:number ?n.
    OPTIONAL {?c table:name ?group_name.}
    }""")
    values = ['Select a value']
    for row in qres:
        to_append = row.NAME
        if row.group_name:
            to_append = '{} ({})'.format(to_append,row.group_name)
        values.append(to_append)
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
    return jsonify({"options":values})

@app.route('/periodictable/classification/<string:clss>', methods=['GET'])
def classification(clss):
    g = rdflib.Graph()
    g.parse("Periodictable.owl")

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
    return jsonify({"options":values})



@app.route('/periodictable/standard_state/<string:state>', methods=['GET'])
def standard_state(state):
    g = rdflib.Graph()
    g.parse("Periodictable.owl")

    qres = g.query(
    """
    PREFIX table:<http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    SELECT (?n as ?NAME)
    {{
    ?c table:standardState table:{}.
    ?c table:name ?n.
    }}""".format(state))
    values = []
    for row in qres:
        values.append(row.NAME)
    return jsonify({"options":values})


@app.route('/periodictable/block/<string:blk>', methods=['GET'])
def block(blk):
    g = rdflib.Graph()
    g.parse("Periodictable.owl")

    qres = g.query(
    """
    PREFIX table:<http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    SELECT (?n as ?NAME)
    {{
    ?c table:block table:{}.
    ?c table:name ?n.
    }}""".format(blk))
    values = []
    for row in qres:
        values.append(row.NAME)
    return jsonify({"options":values})


@app.route('/periodictable/group/<int:gnum>', methods=['GET'])
def group(gnum):
    g = rdflib.Graph()
    g.parse("Periodictable.owl")

    qres = g.query(
    """
    PREFIX table:<http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
    SELECT (?n as ?NAME)
    {{
        ?c table:number "{}"^^xsd:integer.
        ?c table:element ?e.
        ?e table:name ?n.
    }}""".format(gnum))
    values = []
    for row in qres:
        values.append(row.NAME)
    return jsonify({"options":values})


@app.route('/periodictable/period/<int:pnum>', methods=['GET'])
def period(pnum):
    g = rdflib.Graph()
    g.parse("Periodictable.owl")

    qres = g.query(
    """
    PREFIX table:<http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
    SELECT (?n as ?NAME)
    {{
        ?c table:number "{}"^^xsd:integer.
        ?c table:element ?e.
        ?e table:name ?n.
    }}""".format(pnum))
    values = []
    for row in qres:
        values.append(row.NAME)
    return jsonify({"options":values})


@app.route('/periodictable/element/<string:sym>', methods=['GET'])
def element(sym):
    g = rdflib.Graph()
    g.parse("Periodictable.owl")

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


@app.route('/periodictable/multiSelect/', methods=["POST"])
def multiSelect():
    data = dict(request.form)
    print(data)
    where_condition = ""
    if '#classification' in data:
        where_condition += "?c table:classification table:{}.".format(data["#classification"])
    if '#standardState' in data:
        where_condition += "?c table:standardState table:{}.".format(data["#standardState"])
    if '#block' in data:
        where_condition += "?c table:block table:{}.".format(data["#block"])
    if '#group' in data:
        where_condition += """?groupNum table:number "{}"^^xsd:integer.
                        ?groupNum table:element ?c.""".format(data["#group"])
    if '#period' in data:
        where_condition += """?periodNum table:number "{}"^^xsd:integer.
                                ?periodNum table:element ?c.""".format(data["#period"])

    g = rdflib.Graph()
    g.parse("Periodictable.owl")
    print("graph has %s statements." % len(g))
    query =  """
    PREFIX table:<http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
    SELECT (?n as ?NAME)
    {{
        {}
         ?c table:name ?n.
    }}""".format(where_condition)
    print(query)
    qres = g.query(query)
    values = []
    for row in qres:
        values.append(row.NAME)
    return jsonify({"options":values})



def get_results(category):
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
    qres = g.query(query_string)
    return qres

app.run(threaded=True)
