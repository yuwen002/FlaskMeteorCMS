# coding: UTF-8
from flask import render_template
from flask_login import login_required
from app.webmaster import singlepage
from app.models import Category
from app.webmaster.forms.singlepage import ArticleCategoryForm


@singlepage.route('category_show')
@login_required
def category_show():
    categoryAll = Category()
    resCategory = categoryAll.get_category_all()
    form = ArticleCategoryForm()
    return render_template('manage/article_category_show.html', form=form, res_category=resCategory)

@singlepage.route('categoryshow')
@login_required
def category_show():
    categoryAll = Category()
    resCategory = categoryAll.get_category_all()
    form = ArticleCategoryForm()
    return render_template('manage/article_category_show.html', form=form, res_category=resCategory)