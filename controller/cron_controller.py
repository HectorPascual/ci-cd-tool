from .build_controller import create_build
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from app import db
from schemas import CronBuild

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


def get_cron_builds():
    pass