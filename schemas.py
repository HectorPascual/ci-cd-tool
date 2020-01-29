from app import db

class Build(db.Model):

    _id = db.Column(db.Integer, primary_key=True) # ID in database (is unique)
    id = db.Column(db.Integer) # ID in job, together with job_id is an unique tuple
    description = db.Column(db.Text)
    commands = db.Column(db.Text)
    output= db.Column(db.Text)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"))
    node_id = db.Column(db.Integer, db.ForeignKey("node.id"))

    def to_dict(self):
        return {
            'id' : self.id,
            'description': self.description,
            'commands': self.commands,
            'output': self.output,
            'job_id': self.job_id,
            'node_id': self.node_id
        }
    def __repr__(self):
        return f"<id {self.id}, description : {self.description}>"

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)

    builds = db.relationship('Build', backref='job', lazy = False)

    def to_dict(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'description': self.description
        }

    def __repr__(self):
        return f"<id {self.id}, description : {self.description}>"

class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workspace = db.Column(db.Text)
    ip_addr = db.Column(db.Text)
    proto= db.Column(db.Text)

    builds = db.relationship('Build', backref='node', lazy = False)

    def to_dict(self):
        return {
            'id' : self.id,
            'workspace' : self.workspace,
            'ip_addr': self.ip_addr,
            'proto' : self.proto
        }
    def __repr__(self):
        return f"<id {self.id}, @IP : {self.description}>"

# Create tables
db.create_all()
