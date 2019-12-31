# coding: UTF-8
from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from app.webmaster import article_blueprint
from app.models import ArticleCategory, Article
from app.webmaster.forms.article import ArticleCategoryForm, ArticleCategoryEditForm, ArticleForm
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
    category_info = category.get_category(category_id)
    form = ArticleCategoryEditForm()

    if form.validate_on_submit():
        category_name = ArticleCategory.query.filter(ArticleCategory.name == form.name.data, ArticleCategory.id != category_id).first()
        if category_name is None:
            category_info.name = form.name.data

            img = form.img.data
            if img:
                upload_path, img_path = upload_mkdir(img.filename)
                img.save(upload_path)
                category_info.img = img_path

            db.session.commit()

            return redirect(url_for('article.category_list'))
        else:
            flash('分类名称已存在')

    form.name.data = category_info.name

    return render_template('article/category_edit.html', form=form, category=category_info)


@article_blueprint.route('/cagtgory_delete/<int:category_id>')
@login_required
def category_delete(category_id):
    category = ArticleCategory.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()

    return redirect(url_for('article.category_list'))


@article_blueprint.route('/article_add', methods=['GET', 'POST'])
@login_required
def article_add():
    form = ArticleForm()
    if form.validate_on_submit():
        title = form.title.data
        short_title = form.short_title.data
        category_id = form.category_id.data
        synopsis = form.synopsis.data
        author = form.author.data
        article_date = form.article_date.data
        sort = form.sort.data
        recommend = form.recommend.data
        tag = form.tag.data
        source = form.source.data
        img = form.img.data
        content = form.content.data
        comment_on_status = form.comment_on_status.data
        seo_title = form.seo_title.data
        seo_keyword = form.seo_keyword.data
        seo_description = form.seo_description.data

        # 图片上传
        img_path = ''
        if img:
            upload_path, img_path = upload_mkdir(img.filename)
            img.save(upload_path)

        article = Article(
            title=title,
            short_title=short_title,
            category_id=category_id,
            synopsis=synopsis,
            author=author,
            article_date=article_date,
            sort=sort,
            recommend=recommend,
            source=source,
            tag=tag,
            img=img_path,
            content=content,
            comment_on_status=comment_on_status,
            seo_title=seo_title,
            seo_keyword=seo_keyword,
            seo_description=seo_description
        )

        db.session.add(article)
        db.session.commit()

        return redirect(url_for('article.article_list'))

    return render_template('article/article_add.html', form=form)


@article_blueprint.route('article_list', methods=['GET'])
@login_required
def article_list():

    return render_template('article/article_list.html')


def article_edit():
    pass


def article_delete():
    pass