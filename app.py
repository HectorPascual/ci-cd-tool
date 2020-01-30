from flask import Flask
import logging
import os
basedir = os.path.abspath(os.path.dirname(__file__))
from api import api_blueprint
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

app.register_blueprint(api_blueprint)
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=False)

