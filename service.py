#!/usr/bin/env python

from flask import Flask
from flask import jsonify
from flask import request
from flask import abort
from flask import g
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
import psycopg2
import psycopg2.extras

def make_json_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response

app = Flask(__name__)

for code in default_exceptions.items():
    app.error_handler_spec[None][code[0]] = make_json_error

@app.before_request
def before_request():
    g.db = psycopg2.connect(host=app.config['host'], port=app.config['port'], database=app.config['database'],
                            user=app.config['username'], password=app.config['password'])

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/api/variables', methods=['GET'])
def get_variables():
    cur = g.db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT id, name_id, name, validated, min, max FROM variables;')
    variables = cur.fetchall()
    cur.close()
    return jsonify({'variables': variables})

@app.route('/api/variables/<int:variable_id>', methods=['GET'])
def get_variable(variable_id):
    cur = g.db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT TOP 1 id, name_id, name, validated, min, max FROM variables WHERE id = %s;', (variable_id,))
    variable = cur.fetchone()
    cur.close()
    if variable:
        return jsonify({'variable': variable})
    abort(404)

@app.route('/api/variables', methods=['POST'])
def create_variable():
    if not request.json:
        abort(400)
    # TODO: which fields are required?
    if not 'name_id' in request.json or int(request.json['name_id']) <= 0 or not 'name' in request.json:
        abort(400)
    cur = g.db.cursor()
    cur.execute('SELECT id FROM groups WHERE id = %s LIMIT 1;', (request.json['name_id'],))
    if not cur.fetchone():
        abort(400)
    if not 'min' in request.json or not 'max' in request.json or float(request.json['min']) > float(request.json['max']):
        abort(400)
    cur.execute('INSERT INTO variables (name_id, name, validated, min, max) VALUES (%s, %s, %s, %s, %s) RETURNING id;', 
            (request.json['name_id'], request.json['name'], False, request.json['min'], request.json['max']))
    variable_id = cur.fetchone()
    cur.close()
    if variable_id:
        g.db.commit()
        return jsonify(), 201, {'location': '/api/variables/%d' % variable_id}
    abort(500)

@app.route('/api/variables/<int:variable_id>', methods=['PUT'])
def update_variable(variable_id):
    cur = g.db.cursor()
    cur.execute('SELECT id FROM variables WHERE id = %s LIMIT 1;', (variable_id,))
    if not cur.fetchone():
        abort(404)
    # TODO:
    if not request.json:
        abort(400)
    cur = g.db.cursor()
    cur.execute('UPDATE variables SET name = %s, validated = %s, min = %s, max = %s WHERE id = %s;', 
            (request.json['name'], request.json['validated'], request.json['min'], request.json['max'], variable_id,))
    cur.close()
    g.db.commit()
    return jsonify(), 200

@app.route('/api/variables/<int:variable_id>', methods=['DELETE'])
def delete_variable(variable_id):
    cur = g.db.cursor()
    cur.execute('SELECT id FROM variables WHERE id = %s LIMIT 1;', (variable_id,))
    if not cur.fetchone():
        abort(404)
    cur.execute('DELETE FROM variables WHERE id = %s;', (variable_id,))
    cur.close()
    g.db.commit()
    return jsonify(), 200

def evalNode(node_id, value, cur):
    cur.execute('SELECT types.name FROM nodes, types WHERE nodes.type_id = types.id AND nodes.id = %s;', (node_id,))
    node_type = cur.fetchone()[0]
    return 1.0

@app.route('/api/tasks', methods=['POST'])
def create_task():

    cur = g.db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT id, min, max FROM variables;')
    variables = cur.fetchall()
    cur.close()

    for pair in request.json['inputs']:
        valid = False
        for variable in variables:
            if pair['variable'] == variable['id']:
                if pair['value'] >= variable['min'] and pair['value'] <= variable['max']:
                    valid = True
                    break
        if not valid:
            abort(400)

    valid = False
    for variable in variables:
        if request.json['output'] == variable['id']:
            valid = True
            break
    if not valid:
        abort(400)

    cur = g.db.cursor();
    cur.execute('SELECT id FROM rules WHERE rules.validated = True;')
    rules = cur.fetchall()

    count = 0
    output_values = []

    for rule in rules:

        cur.execute('SELECT nodes.variable_id, nodes.parent_id FROM nodes, closures, types, rules WHERE rules.id = %s AND closures.ancestor_id = rules.consequent_id AND nodes.id = closures.descendant_id AND nodes.type_id = types.id AND types.name = %s;', (rule, 'variable'));
        output = cur.fetchone()

        if request.json['output'] != output[0]:
            continue

        cur.execute('SELECT nodes.variable_id, nodes.parent_id FROM nodes, closures, types, rules WHERE rules.id = %s AND closures.ancestor_id = rules.antecedent_id AND nodes.id = closures.descendant_id AND nodes.type_id = types.id AND types.name = %s;', (rule, 'variable'));
        inputs = cur.fetchall()

        if len(request.json['inputs']) != len(inputs):
            continue

        match = True
        for pair in request.json['inputs']:
            found = False
            for variable in inputs:
                if pair['variable'] == variable[0]:
                    found = True
                    break
            if not found:
                match = False
                break
        if not match:
            continue

        cutoff = 1

        for variable in inputs:

            cur.execute('SELECT nodes.id FROM nodes, types WHERE nodes.parent_id = %s AND nodes.type_id != types.id AND types.name = %s;', (variable[1], 'variable'));
            value = cur.fetchone()

            for pair in request.json['inputs']:
                if pair['variable'] == variable[0]:
                    break

            grade = evalNode(value, pair['value'], cur)
            if grade < cutoff:
                cutoff = grade

        cur.execute('SELECT nodes.id FROM nodes, types WHERE nodes.parent_id = %s AND nodes.type_id != types.id AND types.name = %s;', (output[1], 'variable'));
        value = cur.fetchone()

        output_values.append([value[0], cutoff])

        count += 1

    if count == 0:
        abort(404)

    cur.execute('SELECT terms.points FROM variables_terms, terms WHERE variables_terms.variable_id = %s AND variables_terms.term_id = terms.id;', (request.json['output'],))
    points = cur.fetchall()
    arg_min = arg_max = 0.0
    for group in points:
        arg_min = min(arg_min, float(group[0].split(';')[0]))
        arg_max = max(arg_max, float(group[0].split(';')[-1]))

    dividend = divisor = 0.0
    step = ((arg_max - arg_min) / 100)
    arg = arg_min
    while arg <= arg_max:
        grade = 0.0
        for value in output_values:
            grade = max(grade, evalNode(value[0], arg, cur), value[1]) 
        dividend += grade * arg
        divisor += grade
        arg += step

    cur.close()

    return jsonify({'output': dividend / divisor})
