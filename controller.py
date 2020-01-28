from schemas.job import Job


# jobs = [
#     job.Job("Test Job", "this is a test job"),
#     job.Job("Test Job 2", "this is a second test job"),
#     job.Job("Test Job 3", "this is a third test job")
# ]
#
# nodes = [
#     Node('localhost','/home/hector')
# ]

def get_jobs():
    jobs = Job.query.all()
    return jobs

# def get_nodes():
#     nodes = Node.query.all()
#     return nodes
#
# def create_job(title, description):
#     db.session.add(Job(id=1,title=title,description=description))
#     db.session.commit()
#     #new_job = job.Job(title, description)
#     #jobs.append(new_job)
#     #return new_job
#
# def get_builds(job_id):
#     return jobs[job_id].builds
#
# def create_build(job_id, commands):
#     build = jobs[job_id].create_build(description=f"This is a test build for job {job_id}",
#                                       commands=commands, node=nodes[0])
#     build.run_build()
#     return build