import datetime
from app import db

class Build(db.Model):

    _id = db.Column(db.Integer, primary_key=True) # ID in database (is unique)
    id = db.Column(db.Integer) # ID in job, together with job_id is an unique tuple
    description = db.Column(db.Text)
    commands = db.Column(db.Text)
    output= db.Column(db.Text)
    status = db.Column(db.String(32))
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"))
    node_id = db.Column(db.Integer, db.ForeignKey("node.id"))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def to_dict(self):
        return {
            'id' : self.id,
            'description': self.description,
            'commands': self.commands,
            'output': self.output,
            'status' : self.status,
            'job_id': self.job_id,
            'node_id': self.node_id,
            'created_date': self.created_date.strftime("%m/%d/%Y, %H:%M:%S")

        }
    def __repr__(self):
        return f"<id {self.id}, description : {self.description}>"

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    builds = db.relationship('Build', backref='job', lazy = False)

    def to_dict(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'description': self.description,
            'created_date': self.created_date.strftime("%m/%d/%Y, %H:%M:%S")
        }

    def __repr__(self):
        return f"<id {self.id}, description : {self.description}>"

class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workspace = db.Column(db.Text)
    ip_addr = db.Column(db.Text)
    port = db.Column(db.Integer)
    user = db.Column(db.String(64))
    password = db.Column(db.String(64))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    builds = db.relationship('Build', backref='node', lazy = False)

    def to_dict(self):
        return {
            'id' : self.id,
            'workspace' : self.workspace,
            'ip_addr': self.ip_addr,
            'user' : self.user,
            'created_date': self.created_date.strftime("%m/%d/%Y, %H:%M:%S")

        }
    def __repr__(self):
        return f"<id {self.id}, @IP : {self.ip_addr}>"

# Create tables
db.create_all()
