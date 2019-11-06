# coding: UTF-8
import os
from flask import current_app, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_ckeditor import CKEditor

db = SQLAlchemy()
migrate = Migrate()
ckeditor = CKEditor()

login_manager = LoginManager()
login_manager.login_view = 'master.login'
login_manager.login_message = '请登录进入本页。'
login_manager.session_protection = 'strong'


@login_manager.user_loader
def load_user(user_id):
    from app.models import MasterUser
    return MasterUser.query.get(int(user_id))


def get_file_init(app):
    @app.route('/uploads/<path:filename>')
    def get_file(filename):
        return send_from_directory(current_app.config['UPLOAD_PATH'], filename)
