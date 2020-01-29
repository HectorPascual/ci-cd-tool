from schemas import Job
from schemas import Node
from schemas import Build
from app import db
import json
import subprocess


def get_jobs(job_id=None):
    try :
        if job_id :
            job = Job.query.get(job_id)
            job_json = json.dumps(job.to_dict())
            return job_json
        else:
            jobs = Job.query.all()
            jobs_json = json.dumps([job.to_dict() for job in jobs])
            return jobs_json
    except Exception as e:
        return json.dumps([])


def get_nodes(node_id=None):
    try :
        if node_id:
            node = Node.query.get(node_id)
            node_json = json.dumps(node.to_dict())
            return node_json
        else:
            nodes = Node.query.all()
            nodes_json=json.dumps([node.to_dict() for node in nodes])
            return nodes_json
    except Exception as e:
        print(e)
        return json.dumps([])


def get_builds(job_id, build_id=None):
    try :
        if build_id:
            build = Build.query.filter_by(job_id=job_id, id=build_id).first()
            build_json=json.dumps(build.to_dict())
            return build_json
        else:
            builds = Build.query.filter_by(job_id=job_id)
            builds_json=json.dumps([build.to_dict() for build in builds])
            return builds_json
    except Exception as e:
        print(e)
        return json.dumps([])


def create_job(title, description):
     db.session.add(Job(title=title,description=description))
     db.session.commit()

def create_build(job_id, commands, node_id, description):
    job = Job.query.get(job_id)
    id = len(job.builds) + 1

    output = run_on_node(commands, node_id)
    db.session.add(Build(id = id, job_id=job_id, commands=commands, output = output,
                         node_id = node_id, description = description))
    db.session.commit()

def create_node(workspace, ip_addr, proto):
    db.session.add(Node(workspace=workspace, ip_addr=ip_addr, proto=proto))
    db.session.commit()

def delete_job(job_id):
    try:
        job = Job.query.get(job_id)
        db.session.delete(job)
    except Exception as e:
        return json.dumps([])

def delete_node(node_id):
    try :
        node = Node.query.get(node_id)
        db.session.delete(node)
    except Exception as e:
        return json.dumps([])



def run_on_node(commands, node_id):
    node = Node.query.get(node_id)
    output = ""
    cmd_list = commands.split(';')
    for cmd in cmd_list:
        output += subprocess.check_output(f"cd {node.workspace};{cmd}", shell=True).decode('utf-8')
        return output