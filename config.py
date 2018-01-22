# coding=utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    系统的配置文件
    """
    SECRET_KEY = 'zheshiyigebeishangdedongtian'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.91smart.top'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'qyq@91smart.top'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '19921226qyq...'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <qyq@91smart.top>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASKY_POSTS_PER_PAGE = 20

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
   # DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql+pymysql://qyq:123456@192.168.38.128:3306/blogger'


class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql+pymysql://qyq:123456@192.168.38.128:3306/blogger'


config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
}