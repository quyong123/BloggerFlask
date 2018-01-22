# coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_mail import Mail
from flask.ext.pagedown import PageDown
from flask_moment import Moment
mail = Mail()

db = SQLAlchemy(use_native_unicode='utf8')
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
pagedown = PageDown()
moment = Moment()
def create_app(config_name):
    app =Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    db.init_app(app)
    csrf = CSRFProtect(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    moment.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')

    return app