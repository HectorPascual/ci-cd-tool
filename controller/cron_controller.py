from .build_controller import create_build
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from app import db
from schemas import CronBuild
import json

scheduler = BackgroundScheduler() # Scheduler for cron builds
logger = logging.getLogger('root')


def create_cron(cron_exp, cron_key, job_id, commands, node, description):

    minute, hour, day_month, month, day_week = cron_exp.split(' ')
    kwargs = {
        'job_id' : job_id,
        'commands' : commands,
        'node_id' : node,
        'description': description
    }
    cron_build = CronBuild(cron_exp=cron_exp, cron_key=cron_key, job_id=job_id, commands=commands
                           , node_id=node, build_description=description)
    logger.info(f"[DB Access] Creating cron build with key {cron_key} and expression {cron_exp}")
    db.session.add(cron_build)
    db.session.commit()

    scheduler.add_job(func=create_build, kwargs=kwargs, trigger="cron", minute=minute,
                      hour=hour, day=day_month, month=month, day_of_week=day_week, id=cron_key)
    scheduler.start()
    logger.info(f"Started scheduling build in job {job_id} and node {node}")


def get_cron_builds(cron_key = None):
    try:
        if cron_key:
            logger.info(f"[DB Access] Getting cron build with key {cron_key}")
            cron = CronBuild.query.filter_by(cron_key=cron_key).first()
            cron_json = json.dumps(cron.to_dict())
            return cron_json
        else:
            logger.info(f"[DB Access] Getting all cron builds")
            crons = CronBuild.query.all()
            crons_json = json.dumps([cron.to_dict() for cron in crons])
            return crons_json
    except Exception as e:
        logger.warning(f"[DB Access] There was a problem trying to get cron builds\n{e}")
        return json.dumps([])


def delete_cron(cron_key):
    try:
        cron = CronBuild.query.get(cron_key)
        logger.info(f"Stopping cron build with key : {cron_key}")
        scheduler.remove_job(cron_key)
        logger.info(f"[DB Access] Deleting cron build : {cron}")
        db.session.delete(cron)
        db.session.commit()
    except Exception as e:
        logger.warning(f"[DB Access] There was a problem trying to get delete builds\n{e}")
        return json.dumps([])