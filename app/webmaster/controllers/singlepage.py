# coding: UTF-8
from flask import render_template
from app.webmaster import singlepage_blueprint


@singlepage_blueprint.route('/category_add')
def category_add():
    return render_template('singlepage/category_add.html')
