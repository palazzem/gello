# -*- coding: utf-8 -*-

"""__init__.py

Create a modular flask application with database.
"""

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown
from celery import Celery
from config import config, Config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    """Initializes a modular flask application:

        - Initializes all the Flask extensions
        - Configures Celery Task queue
        - Hooks up all the blueprints
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    celery.conf.update(app.config)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask.ext.sslify import SSLify
        sslify = SSLify(app)

    from .controllers.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .controllers.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .controllers.repos import repo as repo_blueprint
    app.register_blueprint(repo_blueprint, url_prefix='/repos')

    from .controllers.issues import issue as issue_blueprint
    app.register_blueprint(issue_blueprint, url_prefix='/repos/issues')

    from .controllers.boards import board as board_blueprint
    app.register_blueprint(board_blueprint, url_prefix='/boards')

    from .controllers.pull_requests import pull_request as pr_blueprint
    app.register_blueprint(pr_blueprint, url_prefix='/repos/pull_requests')

    from .controllers.contributors import contributor as contributor_blueprint
    app.register_blueprint(contributor_blueprint, url_prefix='/contributors')

    from .controllers.trello_lists import trello_list as list_blueprint
    app.register_blueprint(list_blueprint, url_prefix='/boards/lists')

    return app
