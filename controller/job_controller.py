import json
import logging
from schemas import Job
from app import db

logger = logging.getLogger('root')

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

def create_job(title, description):
    job = Job(title=title,description=description)
    logger.info(f"[DB Access] Creating job : {job}")
    db.session.add(job)
    db.session.commit()

def delete_job(job_id):
    try:
        job = Job.query.get(job_id)
        logger.info(f"[DB Access] Deleting job : {job}")
        db.session.delete(job)
    except Exception as e:
        return json.dumps([])