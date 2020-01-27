from models.node import Node
from models import job

jobs = [
    job.Job("Test Job", "this is a test job"),
    job.Job("Test Job 2", "this is a second test job"),
    job.Job("Test Job 3", "this is a third test job")
]

def get_jobs():
    return jobs

def create_job(title, description):
    new_job = job.Job(3, title, description)
    jobs.append(new_job)
    return new_job

def get_builds(job_id):
    return jobs[job_id].builds

def create_build(job_id, commands):
    print(commands)
    runner = Node("/home/hector")
    build = jobs[job_id].create_build(description=f"This is a test build for job {job_id}", commands=commands)

    # RUN BUILD AND COLLECT OUTPUT
    build.output = runner.run_commands(build.commands) #hardcoded for now

    return build