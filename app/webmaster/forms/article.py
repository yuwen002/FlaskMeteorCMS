# coding: UTF-8
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired
from app.models import Category

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
        category = Category.query.filter_by(fid=0).first()
        if category is None:
            self.fid.choices = [('0', '顶级分类')]
        else:
            category = Category.query.filter(Category.fid!=0).order_by(Category.lft).all()
            category_list = []
            for v in category:
                if v.depth == 1:
                    category_list.append({"id": v.id, "name": u'┣━'+v.name})
                elif v.depth > 1:
                    category_list.append({"id": v.id, "name": u'┣━'+u'━'*v.depth+v.name})

            self.fid.choices = [(v['id'], v['name']) for v in category_list]


class ArticleCategoryEditForm(FlaskForm):
    name = StringField(u'分类名称', validators=[DataRequired(message=u'分类名称不能为空')])
    sort = StringField(u'排序')