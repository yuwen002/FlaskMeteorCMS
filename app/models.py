# coding: UTF-8
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


# 用户类
class MasterUser(db.Model, UserMixin):
    """后台用户"""
    __tablename__ = 'master_users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    role_id = db.Column(db.SmallInteger, db.ForeignKey("master_roles.id"), default=0, comment='用户角色')
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    login_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<%s (%r)>' % (self.__class__.__name__, self.username)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Role(db.Model):
    """用户角色"""
    __tablename__ = 'master_roles'
    id = db.Column(db.Integer, primary_key=True, comment='自增ID')
    name = db.Column(db.String(20), unique=True, nullable=False)
    remark = db.Column(db.String(200))
    roles = db.relationship('MasterUser', backref='roles', lazy='dynamic')
