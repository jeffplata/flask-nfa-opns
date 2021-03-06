import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_user import UserManager, SQLAlchemyAdapter
from flask_babel import Babel

db = SQLAlchemy()

from app.user_models import User
from app.models import Base

migrate = Migrate()
mail = Mail()
db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter)

bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    mail.init_app(app)
    user_manager.init_app(app)

    bootstrap.init_app(app)

    babel = Babel()
    babel.init_app(app)

    with app.app_context():
        from app.main import bp as main_bp
        app.register_blueprint(main_bp)

        # some custom filters for jinja2
        from .filters import blueprint as filters_bp
        app.register_blueprint(filters_bp)

        # flask-admin
        from app.fadmin import bp as admin_bp
        app.register_blueprint(admin_bp)
        from app.fadmin.controller import admin

        app.config['FLASK_ADMIN_SWATCH'] = 'lumen'
        admin.init_app(app)

        from app.errors import bp as errors_bp
        app.register_blueprint(errors_bp)

        #app specific
        from app.opnforms import bp as opnforms_bp
        app.register_blueprint(opnforms_bp)

    appname = app.config['USER_APP_NAME']

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject=appname+' Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/'+appname+'.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info(appname+' startup')

    return app
