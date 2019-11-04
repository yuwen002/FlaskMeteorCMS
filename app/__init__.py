# coding: UTF-8
import os
from flask import Flask
from app.config import config
from app.extensions import db, login_manager, migrate
from app.webmaster import master_blueprint, singlepage_blueprint
from app.models import MasterUser


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)
    # 注册扩展
    register_extensions(app)
    register_blueprints(app)
    register_shell_context(app)

    return app


# 扩展
def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)


# 注册蓝本
def register_blueprints(app):
    app.register_blueprint(master_blueprint)
    app.register_blueprint(singlepage_blueprint)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(app=app, db=db, MasterUser=MasterUser)
