# coding: UTF-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length


# 用户登入
class MasterLoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='用户名不能为空'), Length(max=32, min=6, message='用户名长度在6~32位之间')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'), Length(min=6, max=32, message='密码长度在6~32位之间')])
    remember_me = BooleanField('记住我')
