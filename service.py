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

    if node_type == 'term':

        cur.execute("""SELECT functions.name, terms.points FROM functions, terms, nodes WHERE 
                    functions.id = terms.function_id AND 
                    terms.id = nodes.term_id AND 
                    nodes.id = %s;""", (node_id,))
        res = cur.fetchone()
        function = res[0]
        points = res[1].split(';')

        if function == 'синглтон':
            if value == float(points[0]):
                return 1
            else:
                return 0
        elif function == 'Z-функция':
            if value <= float(points[0]):
                return 1
            elif value > float(points[0]) and value < float(points[1]):
                return (float(points[1]) - value) / (float(points[1]) - float(points[0]))
            elif value >= float(points[1]):
                return 0
        elif function == 'S-функция':
            if value <= float(points[0]):
                return 0
            elif value > float(points[0]) and value < float(points[1]):
                return (value - float(points[0])) / (float(points[1]) - float(points[0]))
            elif value >= float(points[1]):
                return 1
        elif function == 'треугольник':
            if value <= float(points[0]):
                return 0
            elif value > float(points[0]) and value < float(points[1]):
                return (value - float(points[0])) / (float(points[1]) - float(points[0]))
            elif value == float(points[1]):
                return 1
            elif value > float(points[1]) and value < float(points[2]):
                return (float(points[2]) - value) / (float(points[2]) - float(points[1]))
            elif value >= float(points[2]):
                return 0
        elif function == 'трапеция':
            if value <= float(points[0]):
                return 0
            elif value > float(points[0]) and value < float(points[1]):
                return (value - float(points[0])) / (float(points[1]) - float(points[0]))
            elif value >= float(points[1]) and value <= float(points[2]):
                return 1
            elif value > float(points[2]) and value < float(points[3]):
                return (float(points[3]) - value) / (float(points[3]) - float(points[2]))
            elif value >= float(points[3]):
                return 0

    elif node_type == 'term_and':

        cur.execute('SELECT id FROM nodes WHERE nodes.parent_id = %s;', (node_id,))
        nodes = cur.fetchall()

        minimum = 1
        for node in nodes:
            minimum = min(minimum, evalNode(node[0], value, cur))

        return minimum

    elif node_type == 'term_or':

        cur.execute('SELECT id FROM nodes WHERE nodes.parent_id = %s;', (node_id,))
        nodes = cur.fetchall()

        maximum = 0
        for node in nodes:
            maximum = max(maximum, evalNode(node[0], value, cur))

        return maximum

    elif node_type == 'term_complex':

        cur.execute("""SELECT nodes.id FROM nodes, types WHERE 
                    nodes.type_id != types.id AND
                    nodes.parent_id = %s AND types.name = %s;""", (node_id, 'hedge'))
        x = evalNode(cur.fetchone()[0], value, cur)

        cur.execute("""SELECT hedges.result FROM nodes, types, hedges WHERE 
                    nodes.type_id = types.id AND
                    nodes.hedge_id = hedges.id AND
                    nodes.parent_id = %s AND types.name = %s;""", (node_id, 'hedge'))

        return eval(cur.fetchone()[0])

@app.route('/api/tasks', methods=['POST'])
def create_task():

    cur = g.db.cursor()
    cur.execute('SELECT id FROM rules WHERE rules.validated = True;')
    rules = cur.fetchall()

    output_values = []

    for rule in rules:

        cur.execute('SELECT nodes.variable_id, nodes.parent_id FROM nodes, closures, types, rules WHERE rules.id = %s AND closures.ancestor_id = rules.consequent_id AND nodes.id = closures.descendant_id AND nodes.type_id = types.id AND types.name = %s;', (rule[0], 'variable'));
        output = cur.fetchone()

        if request.json['output'] != output[0]:
            continue

        cur.execute('SELECT nodes.variable_id, nodes.parent_id FROM nodes, closures, types, rules WHERE rules.id = %s AND closures.ancestor_id = rules.antecedent_id AND nodes.id = closures.descendant_id AND nodes.type_id = types.id AND types.name = %s;', (rule[0], 'variable'));
        inputs = cur.fetchall()

        if len(request.json['inputs']) < len(inputs):
            continue

        match = True
        for variable in inputs:
            found = False
            for pair in request.json['inputs']:
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

            cutoff = min(cutoff, evalNode(value[0], pair['value'], cur))

        cur.execute('SELECT nodes.id FROM nodes, types WHERE nodes.parent_id = %s AND nodes.type_id != types.id AND types.name = %s;', (output[1], 'variable'));
        value = cur.fetchone()

        output_values.append([rule[0], value[0], cutoff])

    if len(rules) == 0:
        abort(404)

    cur.execute('SELECT terms.points FROM variables_terms, terms WHERE variables_terms.variable_id = %s AND variables_terms.term_id = terms.id;', (request.json['output'],))
    points = cur.fetchall()
    arg_min = float(points[0][0].split(';')[0])
    arg_max = float(points[0][0].split(';')[-1])
    for group in points:
        arg_min = min(arg_min, float(group[0].split(';')[0]))
        arg_max = max(arg_max, float(group[0].split(';')[-1]))

    dividend = divisor = 0.0
    arg = arg_min
    while arg <= arg_max:
        grade = 0.0
        for value in output_values:
            grade = max(grade, min(evalNode(value[1], arg, cur), value[2])) 
        dividend += grade * arg
        divisor += grade
        if arg_min == arg_max:
            break
        arg += ((arg_max - arg_min) / 100)

    cur.close()

    rules = []
    for value in output_values:
        pair = {}
        pair['id'] = value[0]
        pair['cutoff'] = round(value[2], 3)
        rules.append(pair)

    if divisor == 0:
        abort(400)

    return jsonify({'rules': rules, 'output': round(dividend / divisor, 3)})
