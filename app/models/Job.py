from datetime import datetime as dt
from . import db
from .User import User


class Job(db.Model):
    __tablename__ = 'jobs_status'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR, nullable=False)
    result = db.Column(db.VARCHAR, nullable=True)
    status = db.Column(db.VARCHAR, nullable=False)
    data = db.Column(db.TEXT, nullable=True)
    user_id = db.Column(db.INTEGER, db.ForeignKey('users.id'), nullable=False)
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
    def create(name, data, current_user: User):
        model = Job(name=name, status=Job.PENDING, data=data, created=dt.now(), user_id=current_user.id)
        db.session.add(model)
        db.session.commit()
        return model

    @staticmethod
    def find(idx=None, by=None):
        if idx is None and by is None:
            raise ValueError('One of both argument must be present')
        if by is None:
            return db.session.query(Job).filter(Job.id == idx)
        return db.session.query(Job).filter_by(**by)

    @staticmethod
    def find_one(idx=None, by=None):
        if idx is None and by is None:
            raise ValueError('One of both argument must be present')
        if by is None:
            return db.session.query(Job).filter(Job.id == idx).first()
        return db.session.query(Job).filter(**by).first()

    @staticmethod
    def all():
        return db.session.query(Job).all()
