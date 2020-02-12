# Create the database if not existing
from src.schemas.build import Build
from src.schemas.job import Job
from src.schemas.node import Node
from src.schemas.cron_build import CronBuild
from src.app import db
db.create_all()