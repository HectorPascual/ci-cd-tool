from flask import Blueprint, Response, request
import logging

logger = logging.getLogger('root')

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/jobs', methods=('GET', 'POST'))
def jobs():
    import controller

    if request.method == 'GET':
        response = Response(
            response=controller.get_jobs(),
            status=200,
            mimetype='application/json'
        )
        return response
    elif request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        response = Response(
            response = controller.create_job(title, description),
            status = 200,
            mimetype = 'application/json'
        )
        return response

@api_blueprint.route('/jobs/<int:job_id>', methods=('GET', 'DELETE'))
def job(job_id):
    import controller
    if request.method == 'GET':
        response = Response(
            response=controller.get_jobs(job_id),
            status=200,
            mimetype='application/json'
        )
        return response
    elif request.method == 'DELETE':
        response = Response(
            response=controller.delete_job(job_id),
            status=200,
            mimetype='application/json'
        )
        return response


@api_blueprint.route('/jobs/<int:job_id>/builds', methods=('GET', 'POST'))
def builds(job_id):
    import controller

    if request.method == 'GET':
        response = Response(
            response=controller.get_builds(job_id),
            status=200,
            mimetype='application/json'
        )
        return response
    elif request.method == 'POST':
        commands = request.form['commands']
        node = request.form['node']
        description = request.form['description']
        cron_exp = request.form.get('cron_exp')
        cron_key = request.form.get('cron_key')

        if cron_exp:
            controller.create_cron(cron_exp, cron_key, job_id, commands, node, description)

        response = Response(
            response=controller.create_build(job_id, commands, node, description),
            status=200,
            mimetype='application/json'
        )
        return response

@api_blueprint.route('/jobs/<int:job_id>/builds/<int:build_id>', methods=('GET', 'DELETE')) # Build id is generic not belonging to job id
def build(job_id, build_id):
    import controller
    if request.method == 'GET':
        response = Response(
            response=controller.get_builds(job_id, build_id),
            status=200,
            mimetype='application/json'
        )
        return response
    elif request.method == 'DELETE':
        response = Response(
            response=controller.delete_build(job_id, build_id),
            status=200,
            mimetype='application/json'
        )
        return response

@api_blueprint.route('/nodes', methods=('GET', 'POST'))
def nodes():
    import controller

    if request.method == 'GET':
        response = Response(
            response=controller.get_nodes(),
            status=200,
            mimetype='application/json'
        )
        return response
    elif request.method == 'POST':
        workspace = request.form['workspace']
        ip_addr = request.form['ip_addr']
        port = request.form.get('port')
        user = request.form.get('user')
        password = request.form.get('password')
        response = Response(
            response=controller.create_node(workspace, ip_addr, port, user, password),
            status=200,
            mimetype='application/json'
        )
        return response

@api_blueprint.route('/nodes/<int:node_id>', methods=('GET', 'DELETE')) # Build id is generic not belonging to job id
def node(node_id):
    import controller
    if request.method == 'GET':
        response = Response(
            response=controller.get_nodes(node_id),
            status=200,
            mimetype='application/json'
        )
        return response
    elif request.method == 'DELETE':
        response = Response(
            response=controller.delete_node(node_id),
            status=200,
            mimetype='application/json'
        )
        return response

@api_blueprint.route('/cron_builds')
def cron_builds():
    import controller
    if request.method == 'GET':
        response = Response(
            response=controller.get_cron_builds(),
            status=200,
            mimetype='application/json'
        )
        return response

@api_blueprint.route('/cron_build/<cron_key>', methods=('GET', 'DELETE'))
def cron_build(cron_key):
    import controller
    if request.method == 'GET':
        response = Response(
            response=controller.get_cron_builds(cron_key),
            status=200,
            mimetype='application/json'
        )
        return response
    else :
        response = Response(
            response=controller.delete_cron(cron_key),
            status=200,
            mimetype='application/json'
        )
        return response