import datetime
from app import db


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