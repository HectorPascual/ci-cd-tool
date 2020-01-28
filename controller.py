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
        builds = Build.query.all()
        builds_json=json.dumps([build.to_dict() for build in builds])
        return builds_json
    except Exception as e:
        print(e)
        return json.dumps([])


def create_job(title, description):
     db.session.add(Job(title=title,description=description))
     db.session.commit()

def create_build(job_id, commands, description):
    output = ""
    cmd_list = commands.split(';')
    for cmd in cmd_list:
        output += subprocess.check_output(cmd, shell=True).decode('utf-8')
    db.session.add(Build(job_id=job_id, commands=commands, output = output, description = description))
    db.session.commit()

# def create_build(job_id, commands):
#     build = jobs[job_id].create_build(description=f"This is a test build for job {job_id}",
#                                       commands=commands, node=nodes[0])
#     build.run_build()
#     return build