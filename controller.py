from schemas import Job
from schemas import Node
from schemas import Build
from app import db
from runner import *
import json
import logging

logger = logging.getLogger('root')

# Nodes with connection established
runners = {}

# READ METHODS
def get_jobs(job_id=None):
    try :
        if job_id :
            logger.info(f"[DB Access] Getting job : {job_id}")
            job = Job.query.get(job_id)
            job_json = json.dumps(job.to_dict())
            return job_json
        else:
            logger.info(f"[DB Access] Getting all jobs")
            jobs = Job.query.all()
            jobs_json = json.dumps([job.to_dict() for job in jobs])
            return jobs_json
    except Exception as e:
        logger.warning(f"[DB Access] There was a problem trying to get jobs\n{e}")
        return json.dumps([])


def get_nodes(node_id=None):
    try :
        if node_id:
            logger.info(f"[DB Access] Getting node : {node_id}")
            node = Node.query.get(node_id)
            node_json = json.dumps(node.to_dict())
            return node_json
        else:
            logger.info(f"[DB Access] Getting all nodes")
            nodes = Node.query.all()
            nodes_json=json.dumps([node.to_dict() for node in nodes])
            return nodes_json
    except Exception as e:
        logger.info(f"[DB Access] There was a problem trying to get nodes\n{e}")
        print(e)
        return json.dumps([])


def get_builds(job_id, build_id=None):
    try :
        if build_id:
            logger.info(f"[DB Access] Getting build nº {build_id} of job {job_id}")
            build = Build.query.filter_by(job_id=job_id, id=build_id).first()
            build_json=json.dumps(build.to_dict())
            return build_json
        else:
            logger.info(f"[DB Access] Getting all builds on job {job_id}")
            builds = Build.query.filter_by(job_id=job_id)
            builds_json=json.dumps([build.to_dict() for build in builds])
            return builds_json
    except Exception as e:
        logger.info(f"[DB Access] There was a problem trying to get builds\n{e}")
        return json.dumps([])

# CREATE METHODS
def create_job(title, description):
    job = Job(title=title,description=description)
    logger.info(f"[DB Access] Creating job : {job}")
    db.session.add(job)
    db.session.commit()

def create_build(job_id, commands, node_id, description):
    job = Job.query.get(job_id)
    node = Node.query.get(node_id)

    id = len(job.builds) + 1

    logger.info(f"New build from job {job_id} will run on node : {node_id}")

    if not node.id in runners:
        logging.info(f"The node {node_id} is not a runner (no connection established)")
        if node.ip_addr == 'localhost':
            logging.info(f"Creating a localhost runner for node {node_id}")
            runners[node.id] = RunerLOCALHOST(node)  # Add to runners dict a new instance
        else:
            logging.info(f"Creating an SSH runner for node {node_id} to IP {node.ip_addr} using configured credentials.")
            runner = RunnerSSH(node)
            runner.connect()
            runners[node.id] = runner
    else:
        logging.info(f"The node {node_id} is already a runner (has a connection established)")
    output = runners[int(node_id)].run_commands(commands)

    logger.info(f"[DB Access] Creating build nº : {id} on job {job_id}")
    db.session.add(Build(id = id, job_id=job_id, commands=commands, output = output,
                         node_id = node_id, description = description))
    db.session.commit()

def create_node(workspace, ip_addr, port, user=None, password=None):
    node = Node(workspace=workspace, ip_addr=ip_addr, port=port, user=user, password=password)
    logger.info(f"[DB Access] Creating node : {node}")
    db.session.add(node)
    db.session.commit()


# DELETE METHODS
def delete_job(job_id):
    try:
        job = Job.query.get(job_id)
        logger.info(f"[DB Access] Deleting job : {job}")
        db.session.delete(job)
    except Exception as e:
        return json.dumps([])

def delete_build(job_id, build_id):
    try:
        build = Build.query.filter_by(job_id=job_id, id=build_id).first()
        logger.info(f"[DB Access] Deleting build nº {build_id} from job {job_id}")
        db.session.delete(build)
        db.session.commit()
    except Exception as e:
        return json.dumps([])

def delete_node(node_id):
    try :
        node = Node.query.get(node_id)
        logger.info(f"[DB Access] Deleting node {node_id}")
        db.session.delete(node)
    except Exception as e:
        return json.dumps([])
