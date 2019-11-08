# coding: UTF-8
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app.models import SingleCategory

class SinglepageCategoryEditForm(FlaskForm):
    name = StringField('分类名称', validators=[DataRequired(message='分类名称不能为空')])
    description = StringField('分类描述')
    img = FileField('分类图片', validators=[FileAllowed(['jpg', 'jpeg', 'gif', 'png'], message='上传类型不正确')])


class SinglepageCategoryForm(SinglepageCategoryEditForm):

    def validate_name(self, name):
        category = SingleCategory.query.filter_by(name=name.data).first()
        if category:
            raise ValidationError('分类名称已存在')


class SinglepageForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(message='标题不能为空')])
    single_category_id = SelectField(
        '单页分类',
        render_kw = {
            "data-am-selected": "{btnSize:'sm'}"
        }
    )
    content = CKEditorField('内容')

    def __init__(self, *args, **kwargs):
        super(SinglepageForm, self).__init__(*args, **kwargs)
        category = SingleCategory.query.order_by(SingleCategory.id.desc()).all()

        if category is None:
            self.single_category_id.choices = [('0', '无分类')]
        else:
            category_list = [{'id': 0, 'name': '无分类'}]
            for v in category:
                category_list.append({'id': v.id, 'name': v.name})

        self.single_category_id.choices = [(v['id'], v['name']) for v in category_list]
