# coding: UTF-8
import os
from datetime import datetime
from flask import render_template, current_app, redirect,  url_for, request, session, flash
from app.webmaster import singlepage_blueprint
from app.webmaster.forms.singlepage import SinglepageCategoryForm, SinglepageCategoryEditForm
from app.helpers import random_filename, mkdir
from app.models import SingleCategory
from app.extensions import db




@singlepage_blueprint.route('/category_add', methods=['GET', 'POST'])
def category_add():
    form = SinglepageCategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        img = form.img.data
        if img:
            # 处理上传文件路径
            today_path = datetime.now().strftime("%Y%m%d");
            img_name = random_filename(img.filename)
            img_path = os.path.join(today_path, img_name).replace('\\', '/')
            upload_path = os.path.join(current_app.config['UPLOAD_PATH'], today_path)
            mkdir(upload_path)
            upload_path = os.path.join(upload_path, img_name)
            # 上传文件
            img.save(upload_path)
            singlepage_category = SingleCategory(name=name, description=description, img=img_path)
        else:
            singlepage_category = SingleCategory(name=name, description=description)

        db.session.add(singlepage_category)
        db.session.commit()
        return redirect(url_for('singlepage.category_list'))

    return render_template('singlepage/category_add.html', form=form)


@singlepage_blueprint.route('/category_list')
def category_list():
    page = request.args.get('page', 1, type=int)
    limit = 20
    paginate = SingleCategory.query.order_by(SingleCategory.id.desc()).paginate(page, per_page=limit, error_out=False)
    categorys = paginate.items
    session['singlepage_category_list_path'] = request.full_path

    return render_template('singlepage/category_list.html', categorys=categorys, paginate=paginate)


@singlepage_blueprint.route('/category_edit/<int:category_id>', methods=['GET', 'POST'])
def category_edit(category_id):
    category = SingleCategory.query.get_or_404(category_id)
    form = SinglepageCategoryEditForm()

    if form.validate_on_submit():
        is_name = SingleCategory.query.filter(SingleCategory.name == form.name.data, SingleCategory.id != category_id).first()
        if is_name is None:
            category.name = form.name.data
            category.description = form.description.data
            img = form.img.data
            if img:
                # 处理上传文件路径
                today_path = datetime.now().strftime("%Y%m%d");
                img_name = random_filename(img.filename)
                img_path = os.path.join(today_path, img_name).replace('\\', '/')
                upload_path = os.path.join(current_app.config['UPLOAD_PATH'], today_path)
                mkdir(upload_path)
                upload_path = os.path.join(upload_path, img_name)
                # 上传文件
                img.save(upload_path)
                category.img = img_path

            db.session.commit()
        else:
            flash('分类名称已存在')

        path = session.get('singlepage_category_list_path')
        # if path:
        #     endpoint = path
        # else:
        #     endpoint = url_for('singlepage.category_list')
        endpoint = path if path else url_for('singlepage.category_list')
        return redirect(endpoint)

    form.name.data = category.name
    form.description.data = category.description

    return render_template('singlepage/category_edit.html', form=form, category=category)


@singlepage_blueprint.route('/category_delete/<int:category_id>')
def category_delete(category_id):
    category = SingleCategory.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()

    return redirect(url_for('singlepage.category_list'))


@singlepage_blueprint.route('/singlepage_add')
def singlepage_add():
    pass


@singlepage_blueprint.route('/singlepage_list')
def singlepage_list():
    pass


@singlepage_blueprint.route('/singlepage_edit/<int:single_id>')
def singlepage_edit(single_id):
    pass


@singlepage_blueprint.route('/singlepage_delete/<int:single_id>')
def singlepage_delete(single_id):
    pass
