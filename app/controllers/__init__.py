from . import UserController, JobController


def init_app(app):
    app.register_blueprint(UserController.bp)
    app.register_blueprint(JobController.bp, url_prefix='/job')
