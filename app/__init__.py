from flask import Flask
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from app.models import db
import os


class Config(object):
    SECRET_KEY = os.urandom(24)

    SERVER_NAME = 'baloo.local:5000'

    WTF_CSRF_SECRET_KEY = 'qwe7fds[123]ds12fd[123$@'

    SESSION_COOKIE_SECURE = False

    SESSION_COOKIE_NAME = 'WTI-REST-WebSession'

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:projekt-REST-wti-2020@localhost:5432/projekt-rest'

    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__, instance_relative_config=True, template_folder='./templates')
app.config.from_object(Config())

db.init_app(app)

login = LoginManager()
# csrf = CSRFProtect()


with app.app_context():
    from . import models, controllers, services, forms

    db.create_all()
    forms.init_app(app)
    models.init_app(app)
    controllers.init_app(app)
    services.init_app(app)

    login.init_app(app)
    login.login_view = 'index.login'
    # csrf.init_app(app)
