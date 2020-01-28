from app import db

class Build(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    commands = db.Column(db.Text)
    output= db.Column(db.Text)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"))

    #node = db.relationship('Node', uselist = False, lazy = True)

    def to_dict(self):
        return {
            'id' : self.id,
            'description': self.description,
            'commands': self.commands,
            'output': self.output,
            'job_id': self.job_id
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
            #'builds': self.builds if len(self.builds) else []
        }

    def __repr__(self):
        return f"<id {self.id}, description : {self.description}>"

class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workspace = db.Column(db.Text)
    ip_addr = db.Column(db.Text)
    proto= db.Column(db.Text)
    #build_id = db.Column(db.Integer, db.ForeignKey("build.id"))

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
