from . import UserController, JobController, TokenController


def init_app(app):
    app.register_blueprint(UserController.bp)
    app.register_blueprint(JobController.bp, url_prefix='/job')
    app.register_blueprint(TokenController.bp, url_prefix='/token')
