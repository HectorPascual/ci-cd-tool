import json

from controller import controller
from flask import Blueprint, Response, request

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/jobs', methods=('GET', 'POST'))
def jobs():
    if request.method == 'GET':
        response = Response(
            response=json.dumps(controller.get_jobs(), default = lambda x: x.__dict__),
            status=200,
            mimetype='application/json'
        )
        return response
    elif request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        response = Response(
            response = json.dumps(controller.create_job(title, description), default = lambda x: x.__dict__),
            status = 200,
            mimetype = 'application/json'
        )
        return response

@api_blueprint.route('/jobs/<job_id>/builds', methods=('GET', 'POST'))
def builds(job_id):
    if request.method == 'GET':
        response = Response(
            response=json.dumps(controller.get_builds(int(job_id)), default = lambda x: x.__dict__),
            status=200,
            mimetype='application/json'
        )
        return response
    elif request.method == 'POST':
        commands = request.form['commands']
        cmd_list = commands.split(';')
        response = Response(
            response=json.dumps(controller.create_build(int(job_id), cmd_list), default = lambda x: x.__dict__),
            status=200,
            mimetype='application/json'
        )
        return response

@api_blueprint.route('/nodes')
def nodes():
    response = Response(
        response=json.dumps(controller.get_nodes(), default=lambda x: x.__dict__),
        status=200,
        mimetype='application/json'
    )
    return response

