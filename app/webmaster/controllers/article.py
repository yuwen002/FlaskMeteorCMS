# coding: UTF-8
from flask import render_template
from flask_login import login_required
from app.webmaster import article_blueprint
from app.models import Category
from app.webmaster.forms.article import ArticleCategoryForm


@article_blueprint.route('/category_list')
@login_required
def category_list():
    categoryAll = Category()
    resCategory = categoryAll.get_category_all()
    form = ArticleCategoryForm()
    return render_template('article/category_show.html', form=form, res_category=resCategory)
