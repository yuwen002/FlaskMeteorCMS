# coding: UTF-8
from flask import render_template
from flask_login import login_required
from app.webmaster import master_blueprint

@master_blueprint.route('category_show')
@login_required
def category_show():
    categoryAll = Categorys()
    resCategory = categoryAll.get_category_all()
    form = ArticleCategoryForm()
    return render_template('manage/article_category_show.html', form=form, res_category=resCategory)