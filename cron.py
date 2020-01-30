from controller import create_build
from apscheduler.schedulers.background import BackgroundScheduler
import logging

scheduler = BackgroundScheduler() # Scheduler for cron builds
logger = logging.getLogger('root')

def cron_build(cron_exp, job_id, commands, node, description):
    minute, hour, day_month, month, day_week = cron_exp.split(' ')
    kwargs = {
        'job_id' : job_id,
        'commands' : commands,
        'node_id' : node,
        'description': description
    }
    scheduler.add_job(func=create_build, kwargs=kwargs, trigger="cron", minute=minute,
                      hour=hour, day=day_month, month=month, day_of_week=day_week)
    logger.info(f"Started scheduling build in job {job_id} and node {node}")
    scheduler.start()