# coding: UTF-8
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app.models import ArticleCategory

class ArticleCategoryForm(FlaskForm):
    name = StringField('分类名称', validators=[DataRequired(message=u'分类名称不能为空')])
    sort = StringField('排序')
    fid = SelectField(
        '上级分类',
        coerce=int,
        render_kw={
            "data-am-selected": "{btnSize:'sm'}"
        }
    )
    img = FileField('分类图片', validators=[FileAllowed(['jpg', 'jpeg', 'gif', 'png'], message='上传类型不正确')])

    def __init__(self, *args, **kwargs):
        super(ArticleCategoryForm, self).__init__(*args, **kwargs)
        category = ArticleCategory.query.filter_by(fid=0).first()
        if category is None:
            self.fid.choices = [('0', '顶级分类')]
        else:
            category = ArticleCategory.query.order_by(ArticleCategory.lft).all()
            category_list = []
            for v in category:
                if v.depth == 0:
                    category_list.append({"id": v.id, "name": v.name})
                elif v.depth == 1:
                    category_list.append({"id": v.id, "name": '┣━' + v.name})
                elif v.depth > 1:
                    category_list.append({"id": v.id, "name": '┣━' + '━' * v.depth + v.name})

            self.fid.choices = [(v['id'], v['name']) for v in category_list]

    def validate_name(self, name):
        category = ArticleCategory.query.filter_by(name=name.data).first()
        if category:
            raise ValidationError('该分类已存在')

class ArticleCategoryEditForm(FlaskForm):
    name = StringField(u'分类名称', validators=[DataRequired(message=u'分类名称不能为空')])
    sort = StringField(u'排序')
    img = FileField('分类图片', validators=[FileAllowed(['jpg', 'jpeg', 'gif', 'png'], message='上传类型不正确')])
