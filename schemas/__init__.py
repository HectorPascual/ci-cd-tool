from .build import Build
from .cron_build import CronBuild
from .job import Job
from .node import Node

# Create the database if not existing
from app import db
db.create_all()