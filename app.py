from flask import Flask
import os
basedir = os.path.abspath(os.path.dirname(__file__))
from api.api_routes import api_blueprint
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

app.register_blueprint(api_blueprint)
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)

