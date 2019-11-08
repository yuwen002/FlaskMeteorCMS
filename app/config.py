# coding: UTF-8
import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig(object):
    SECRET_KEY = 'SHERRY_LIUXINGYU_CMS'

    # 上传文件大小
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    # 上传路径
    UPLOAD_PATH = os.path.join(basedir, 'uploads')

    # CKEditor配置
    # CKEditor包类型，可选值为 basic、standard、full
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_PKG_TYPE = 'standard'
    CKEDITOR_LANGUAGE = 'zh-cn'
    CKEDITOR_FILE_UPLOADER = 'master.ckupload'
    CKEDITOR_HEIGHT = '500'
    CKEDITOR_WIDTH = '0'


    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False
    CSRF_ENABLED = True
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
