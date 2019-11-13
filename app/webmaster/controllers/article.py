# coding: UTF-8
from flask import render_template, redirect, url_for
from flask_login import login_required
from app.webmaster import article_blueprint
from app.models import ArticleCategory
from app.webmaster.forms.article import ArticleCategoryForm
from app.helpers import upload_mkdir
from app.extensions import db


@article_blueprint.route('/category_list')
@login_required
def category_list():
    category_all = ArticleCategory()
    res_category = category_all.get_category_all()

    return render_template('article/category_list.html', res_category=res_category)


@article_blueprint.route('/category_add', methods=['GET', 'POST'])
@login_required
def category_add():
    form = ArticleCategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        fid = form.fid.data
        img = form.img.data

        img_path = ''
        if img:
            upload_path, img_path = upload_mkdir(img.filename)
            img.save(upload_path)

        category = ArticleCategory()
        category.add_category(name=name, fid=fid, img=img_path)
        return redirect(url_for('article.category_list'))

    return render_template('article/category_add.html', form=form)


@article_blueprint.route('/category_edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def category_edit(category_id):
    category = ArticleCategory()
    form = ArticleCategoryForm()

    info = category.get_category(category_id)
    form.name.data = info.name

    return render_template('article/category_edit.html', form=form)
