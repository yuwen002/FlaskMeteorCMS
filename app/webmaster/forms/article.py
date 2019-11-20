# coding: UTF-8
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SelectField, DateField, IntegerField, BooleanField
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
    name = StringField('分类名称', validators=[DataRequired(message='分类名称不能为空')])
    sort = StringField('排序')
    img = FileField('分类图片', validators=[FileAllowed(['jpg', 'jpeg', 'gif', 'png'], message='上传类型不正确')])


class ArticleForm(FlaskForm):
    title = StringField('新闻分类', validators=[DataRequired(message='文章标题不能为空')])
    category_id = SelectField(
        '分类',
        coerce=int,
        render_kw={
            "data-am-selected": "{btnSize:'sm'}"
        }
    )
    short_title = StringField('文章短标题')
    external_links = StringField('文章外链')
    synopsis = StringField('文章外链')
    author = StringField('文章作者')
    article_date = DateField('文章日期')
    sort = IntegerField('文章排序')
    recommend = StringField('文章推荐')
    tag = StringField('TAG标签')
    img = FileField('文章图片', validators=[FileAllowed(['jpg', 'jpeg', 'gif', 'png'])])
    content = CKEditorField('内容')
    comment_on_status = BooleanField('评论状态', default=True)
    seo_title = StringField('SEO标题')
    seo_keyword = StringField('SEO关键字')
    seo_description = StringField('SEO描述')

    def __init__(self, *args, **kwargs):
        super(ArticleCategoryForm, self).__init__(*args, **kwargs)
        category = ArticleCategory()
        category_all = category.get_category_all()

        category_list = []
        for v in category_all:
            if v.depth == 0:
                category_list.append({"id": v.id, "name": v.name})
            elif v.depth == 1:
                category_list.append({"id": v.id, "name": '┣━' + v.name})
            elif v.depth > 1:
                category_list.append({"id": v.id, "name": '┣━' + '━' * v.depth + v.name})

        self.fid.choices = [(v['id'], v['name']) for v in category_list]
