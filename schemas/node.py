import datetime
from app import db

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