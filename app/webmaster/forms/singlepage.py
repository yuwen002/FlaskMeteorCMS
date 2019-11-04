# coding: UTF-8
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, FileField
from wtforms.validators import DataRequired


class SinglepageCategoryForm(FlaskForm):
    name = StringField('分类名称', validators=[DataRequired(message='分类名称不能为空')])
    description = StringField('分类描述')
    img = FileField('分类图片', validators=[])