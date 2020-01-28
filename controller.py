from schemas import Job
from schemas import Node
from schemas import Build
from app import db
import json
import subprocess

def get_jobs():
    try :
        jobs = Job.query.all()
        jobs_json = json.dumps([job.to_dict() for job in jobs])
        print(jobs[0].builds)
        return jobs_json
    except Exception as e:
        return json.dumps([])

def get_nodes():
    try :
        nodes = Node.query.all()
        nodes_json=json.dumps([node.to_dict() for node in nodes])
        return nodes_json
    except Exception as e:
        print(e)
        return json.dumps([])

def get_builds(job_id):
    try :
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
    output = run_on_node(commands, node_id)
    db.session.add(Build(job_id=job_id, commands=commands, output = output, node_id = node_id,
                         description = description))
    db.session.commit()

def create_node(workspace, ip_addr, proto):
    db.session.add(Node(workspace=workspace, ip_addr=ip_addr, proto=proto))
    db.session.commit()

def run_on_node(commands, node_id):
    node = Node.query.get(node_id)
    output = ""
    cmd_list = commands.split(';')
    for cmd in cmd_list:
        output += subprocess.check_output(f"cd {node.workspace};{cmd}", shell=True).decode('utf-8')
        return output