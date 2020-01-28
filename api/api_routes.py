from flask import Blueprint, Response, request

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

@api_blueprint.route('/jobs/<job_id>/builds', methods=('GET', 'POST'))
def builds(job_id):
    import controller

    if request.method == 'GET':
        response = Response(
            response=controller.get_builds(int(job_id)),
            status=200,
            mimetype='application/json'
        )
        return response
    elif request.method == 'POST':
        commands = request.form['commands']
        node = request.form['node']
        description = request.form['description']
        response = Response(
            response=controller.create_build(int(job_id), commands, node, description),
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
        proto = request.form['proto']
        response = Response(
            response=controller.create_node(workspace, ip_addr, proto),
            status=200,
            mimetype='application/json'
        )
        return response

