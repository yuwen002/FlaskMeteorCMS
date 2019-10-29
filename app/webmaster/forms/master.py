# coding: UTF-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from app.models import MasterUser


# 用户登入
class MasterLoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='用户名不能为空'), Length(max=32, min=6, message='用户名长度在6~32位之间')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'), Length(min=6, max=32, message='密码长度在6~32位之间')])
    remember_me = BooleanField('记住我')


# 用户注册
class RegisterUserForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='用户名不能为空'), Length(max=32, min=6, message='用户名长度在6~32位之间')])
    password = PasswordField('密码', validators=[DataRequired(message='密码用户名不能为空'), Length(min=6, max=32, message='密码长度在6~32位之间')])
    confirm_password = PasswordField('确认密码', validators=[DataRequired(message='确认密码不能为空'), EqualTo('password', message='两次密码不一致')])
    email = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空'), Email(message='无效的邮箱格式')])

    # 验证用户名是否存在
    def validate_username(self, username):
        master_user = MasterUser.query.filter_by(username=username.data).first()
        if master_user:
            raise ValidationError('用户名已注册，请选用其它名称')

    # 验证邮箱是否存在
    def validate_email(self, email):
        master_user = MasterUser.query.filter_by(email=email.data).first()
        if master_user:
            raise ValidationError('该邮箱已注册使用，请选用其它邮箱')

    # 用户修改密码
    class ModifyUserPasswordForm(FlaskForm):
        old_password = PasswordField('原密码', validators=[DataRequired(message='原密码不能为空')])
        new_password = PasswordField('新密码', validators=[DataRequired(message='新密码不能为空'), Length(min=6, max=32, message='密码长度在6~32位之间')])
        confirm_new_password = PasswordField('确认密码', validators=[DataRequired(message='确认密码不能为空'), EqualTo('new_password', message='两次密码不一致')])


# 用户基本信息修改
class ModifyUserInfoForm(FlaskForm):
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空')])
    email = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空'), Email(message='无效的邮箱格式')])


# 用户修改密码
class ModifyUserPasswordForm(FlaskForm):
    old_password = PasswordField('原密码', validators=[DataRequired(message='原密码不能为空')])
    new_password = PasswordField('新密码', validators=[DataRequired(message='新密码不能为空'), Length(min=6, max=32, message='密码长度在6~32位之间')])
    confirm_new_password = PasswordField('确认密码', validators=[DataRequired(message='确认密码不能为空'), EqualTo('new_password', message='两次密码不一致')])


# 注册用户基本信息修改
class ModifyRegUserInfoForm(FlaskForm):
    username = StringField('用户名')
    password = PasswordField('密码')
    email = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空'), Email(message='无效的邮箱格式')])

    def validate_password(self, password):
        if password.data:
            l = len(password.data)
            if l > 32 or l < 6:
                raise ValidationError('密码长度在6~32位之间')
