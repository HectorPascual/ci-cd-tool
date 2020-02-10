import datetime
from app import db

class CronBuild(db.Model):
    cron_key = db.Column(db.String(32), primary_key=True)
    cron_exp = db.Column(db.String(32))
    build_description = db.Column(db.Text)
    commands = db.Column(db.Text)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"))
    node_id = db.Column(db.Integer, db.ForeignKey("node.id"))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'cron_key' : self.cron_key,
            'build_description': self.build_description,
            'commands': self.commands,
            'job_id': self.job_id,
            'node_id': self.node_id,
            'created_date': self.created_date.strftime("%m/%d/%Y, %H:%M:%S")
        }

    def __repr__(self):
        return f"<cron_key {self.cron_key}>"