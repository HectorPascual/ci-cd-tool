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
        title = request.form['title']
        description = request.form['description']
        response = Response(
            response=controller.create_build(int(job_id), commands   , description),
            status=200,
            mimetype='application/json'
        )
        return response

@api_blueprint.route('/nodes')
def nodes():
    import controller

    response = Response(
        response=controller.get_nodes(),
        status=200,
        mimetype='application/json'
    )
    return response

