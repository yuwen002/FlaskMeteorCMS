# coding: UTF-8
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = 'master.login'
login_manager.login_message = '请登录进入本页。'
login_manager.session_protection = 'strong'


@login_manager.user_loader
def load_user(user_id):
    from app.models import MasterUser
    return MasterUser.query.get(int(user_id))
