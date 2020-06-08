from datetime import datetime as dt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from app import login


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR, nullable=False)
    password_hash = db.Column(db.VARCHAR, nullable=False)
    created = db.Column(db.TIMESTAMP, nullable=False)
    jobs = db.relationship('Job', backref=db.backref('user', lazy=True), lazy=True)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}>"

    def __str__(self):
        return f"User: {self.id}, {self.name}"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def create(name, password):
        model = User(name=name, password_hash=generate_password_hash(password), created=dt.now())
        db.session.add(model)
        db.session.commit()
        return model

    @staticmethod
    def find_one(idx=None, by=None):
        if idx is None and by is None:
            raise ValueError('One of both argument must be present')
        if by is None:
            return db.session.query(User).filter(User.id == idx).first()
        return db.session.query(User).filter_by(**by).first()

    @staticmethod
    def all():
        return db.session.query(User).all()
