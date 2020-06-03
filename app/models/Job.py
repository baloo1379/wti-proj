from datetime import datetime as dt
from . import db


class Job(db.Model):
    __tablename__ = 'jobs_status'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR, nullable=False)
    result = db.Column(db.VARCHAR, nullable=True)
    status = db.Column(db.VARCHAR, nullable=False)
    data = db.Column(db.TEXT, nullable=True)
    created = db.Column(db.TIMESTAMP, nullable=False)

    PENDING = 'pending'
    RUNNING = 'running'
    DONE = 'done'

    def __repr__(self):
        return f"<Job(id={self.id}, name={self.name}, result={self.result}, status={self.status}, " \
               f"data={self.data}, created={self.created})>"

    def __str__(self):
        return f"Job: {self.id}, {self.name}, {self.result}, {self.status}, " \
               f"{self.data}, {self.created}"

    @staticmethod
    def create(name, data):
        model = Job(name=name, status=Job.PENDING, data=data, created=dt.now())
        db.session.add(model)
        db.session.commit()
        return model

    @staticmethod
    def find(idx):
        return db.session.query(Job).filter(Job.id == idx).first()

    @staticmethod
    def all():
        return db.session.query(Job).all()
