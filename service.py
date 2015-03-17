#!/usr/bin/env python

from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

variables = [
    {
        'id': 1,
        'name_id': 1,
        'name': 'первая переменная',
        'validated': True,
        'min': -100.0,
        'max': 100.0
    },
    {
        'id': 2,
        'name_id': 2,
        'name': 'вторая переменная',
        'validated': True,
        'min': 0.0,
        'max': 1.0
    },
    {
        'id': 3,
        'name_id': 3,
        'name': 'третья переменная',
        'validated': False,
        'min': 0.0,
        'max': 0.0
    }
]

@app.route('/api/variables', methods=['GET'])
def get_variables():
    return jsonify({'variables': variables})

@app.route('/api/tasks', methods=['POST'])
def create_task():
    summ = 0
    for pair in request.json['inputs']:
        summ += pair['value']
    return jsonify({'output': summ})

app.run(debug=True)
