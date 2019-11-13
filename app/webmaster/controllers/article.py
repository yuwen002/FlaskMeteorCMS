# coding: UTF-8
from flask import render_template
from flask_login import login_required
from app.webmaster import article_blueprint
from app.models import Category
from app.webmaster.forms.article import ArticleCategoryForm
from app.helpers import upload_mkdir
from app.extensions import db


@article_blueprint.route('/category_list')
@login_required
def category_list():
    categoryAll = Category()
    resCategory = categoryAll.get_category_all()

    return render_template('article/category_show.html', res_category=resCategory)


@article_blueprint.route('/category_add', methods=['GET', 'POST'])
@login_required
def category_add():
    form = ArticleCategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        fid = form.fid.data
        img = form.img.data

        if img:
            upload_path, img_path = upload_mkdir(img.filename)
            img.save(upload_path)
            category = Category(name=name, fid=fid, img=img_path)
        else:
            category = Category(name=name, fid=fid)

        db.session.add(category)
        db.session.commit()

    return render_template('article/category_add.html', form=form)
