from datetime import datetime as dt
from base64 import b64encode
from os import urandom
from . import db


class Token(db.Model):
    __tablename__ = 'tokens'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR, nullable=False)
    api_key_hash = db.Column(db.VARCHAR, nullable=False)
    created = db.Column(db.TIMESTAMP, nullable=False)

    def __repr__(self):
        return f"<Token(id={self.id}, name={self.name}, created={self.created}>"

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def create(name, api_key):
        model = Token(name=name, api_key_hash=api_key, created=dt.now())
        db.session.add(model)
        db.session.commit()
        return model

    @staticmethod
    def generate_api_key():
        return b64encode(urandom(64)).decode('utf-8')

    @staticmethod
    def find_one(idx=None, by=None):
        if idx is None and by is None:
            raise ValueError('One of both argument must be present')
        if by is None:
            return db.session.query(Token).filter(Token.id == idx).first()
        return db.session.query(Token).filter_by(**by).first()

    @staticmethod
    def all():
        return db.session.query(Token).all()
