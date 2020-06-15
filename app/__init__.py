from flask import Flask
from flask_login import LoginManager
from app.models import db
from dotenv import load_dotenv
import os

load_dotenv()


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')

    SERVER_NAME = os.getenv('SERVER_NAME')

    WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY')

    SESSION_COOKIE_SECURE = False

    SESSION_COOKIE_NAME = os.getenv('SERVER_NAME')

    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__, instance_relative_config=True, template_folder='./templates')
app.config.from_object(Config())

db.init_app(app)

login = LoginManager()


with app.app_context():
    from . import models, controllers, services, forms

    login.init_app(app)
    login.login_view = 'index.login'

    db.create_all()
    forms.init_app(app)
    models.init_app(app)
    controllers.init_app(app)
    services.init_app(app)

    from .models.User import User

    @login.user_loader
    def load_user(idx):
        return User.find_one(idx)

