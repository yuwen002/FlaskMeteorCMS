# coding: UTF-8
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required
from app.webmaster import master_blueprint
from app.webmaster.forms.master import MasterLoginForm
from app.models import MasterUser
from app.extensions import db


# 后台管理员登入
@master_blueprint.route('/')
@master_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = MasterLoginForm()
    if form.validate_on_submit():
        master_user = MasterUser.query.filter_by(username=form.username.data).first()
        if master_user is not None and master_user.verify_password(form.password.data):
            master_user.login_at = datetime.now()
            db.session.add(master_user)
            db.session.commit()
            login_user(master_user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('master.welcome'))
        flash('无效的用户名或密码')
    return render_template('master/login.html', form=form)


@master_blueprint.route('/welcome')
@login_required
def welcome():
    return 'welcome'
