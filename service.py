#!/usr/bin/env python

from flask import Flask, jsonify, request, abort, g
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
import psycopg2
import psycopg2.extras
import sys

# force error handlers to response with json instead of html

def make_json_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response

app = Flask(__name__)

for code in default_exceptions.items():
    app.error_handler_spec[None][code[0]] = make_json_error

# manage database connections 

@app.before_request
def before_request():
    g.db = psycopg2.connect(host='127.0.0.1', database='fuzzy', user='user1', password='pass1', cursor_factory=psycopg2.extras.RealDictCursor)

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# request handlers

@app.route('/api/variables', methods=['GET'])
def get_variables():
    cur = g.db.cursor()
    cur.execute('SELECT id, name, name_id, validated, min, max FROM variables;')
    res = cur.fetchall()
    cur.close()
    return jsonify({'variables': res})

@app.route('/api/variables/<int:variable_id>', methods=['GET'])
def get_variable(variable_id):
    cur = g.db.cursor()
    cur.execute('SELECT id, name, name_id, validated, min, max FROM variables WHERE id = %s;', (variable_id,))
    res = cur.fetchall()
    cur.close()
    if res:
        return jsonify({'variable': res})
    abort(404)

# TODO: rework with real database

@app.route('/api/variables', methods=['POST'])
def create_variable():
    variable = {
        'id': variable[-1]['id'] + 1,
        'name_id': request.json['name_id'],
        'name': request.json['name'],
        'validated': request.json['validated'],
        'min': request.json['min'],
        'max': request.json['max']
    }
    variables.append(variable)
    return jsonify({'variable': variable}), 201, {'location': '/api/variables/' % variable['id']}

@app.route('/api/variables/<int:variable_id>', methods=['DELETE'])
def delete_variable(variable_id):
    for variable in variables:
        if variable['id'] == variable_id:
            variables.remove(variable['id'])
            return jsonify(), 200
    abort(404)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    summ = 0
    for pair in request.json['inputs']:
        summ += pair['value']
    return jsonify({'output': summ})

app.run(debug=True)
