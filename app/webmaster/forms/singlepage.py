# coding: UTF-8
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError
from app.models import SingleCategory


class SinglepageCategoryForm(FlaskForm):
    name = StringField('分类名称', validators=[DataRequired(message='分类名称不能为空')])
    description = StringField('分类描述')
    img = FileField('分类图片', validators=[FileAllowed(['jpg', 'jpeg', 'gif', 'png'], message='上传类型不正确')])

    def validate_name(self, name):
        category = SingleCategory.query.filter_by(name=name.data).first()
        if category:
            raise ValidationError('分类名称已存在')
