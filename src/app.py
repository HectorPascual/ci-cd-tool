from flask import Flask
import logging
import os
basedir = os.path.abspath(os.path.dirname(__file__))
from src.api import api_blueprint
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'app.db')

app.register_blueprint(api_blueprint)
db = SQLAlchemy(app)

@app.before_first_request
def init_cron():
    # Must start the cron jobs stored in the database
    from src.controller import start_cron
    from src.schemas import CronBuild
    cron_list = CronBuild.query.all()
    start_cron(cron_list)

