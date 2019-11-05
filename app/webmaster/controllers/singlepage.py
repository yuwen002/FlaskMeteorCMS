# coding: UTF-8
import os
from datetime import datetime
from flask import render_template, current_app, redirect,  url_for, request, session
from app.webmaster import singlepage_blueprint
from app.webmaster.forms.singlepage import SinglepageCategoryForm
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

        # 处理上传文件路径
        today_path = datetime.now().strftime("%Y%m%d");
        img_name = random_filename(img.filename)
        img_path = os.path.join(today_path, img_name)
        upload_path = os.path.join(current_app.config['UPLOAD_PATH'], today_path)
        mkdir(upload_path)
        upload_path = os.path.join(upload_path, img_name)
        # 上传文件
        img.save(upload_path)

        singlepage_category = SingleCategory(name=name, description=description, img=img_path)
        db.session.add(singlepage_category)
        db.session.commit()
        return redirect(url_for('singlepage.category_list'))

    return render_template('singlepage/category_add.html', form=form)


@singlepage_blueprint.route('/category_list')
def category_list():
    page = request.args.get('page', 1, type=int)
    limit = 2
    paginate = SingleCategory.query.order_by(SingleCategory.id.desc()).paginate(page, per_page=limit, error_out=False)
    categorys = paginate.items
    session['singlepage_category_list_path'] = request.full_path

    return render_template('singlepage/category_list.html', categorys=categorys, paginate=paginate)
