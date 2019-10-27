# coding: UTF-8
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from app.webmaster import master_blueprint
from app.webmaster.forms.master import MasterLoginForm, RegisterUserForm, ModifyUserInfoForm, ModifyUserPasswordForm
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


# 后台用户注册
@master_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        # post 字段
        username = form.username.data
        password = form.password.data
        email = form.email.data

        # 注册用户数据写入
        master_user = MasterUser(username=username, password=password, email=email)
        db.session.add(master_user)
        db.session.commit()

        flash('注册成功')
        return redirect(url_for('master.login'))

    return render_template('master/register.html', form=form)


# 登入欢迎页面
@master_blueprint.route('/welcome')
@login_required
def welcome():
    return render_template('master/welcome.html')


# 登出
@master_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经注销了。')
    return redirect(url_for('master.login'))


@master_blueprint.route('/user_info')
@login_required
def user_info():
    form_info = ModifyUserInfoForm()
    form_password = ModifyUserPasswordForm()

    return render_template('master/modify_user_info.html', form_password=form_password, form_info=form_info)


@master_blueprint.route('/modify_user_info', methods=['POST'])
@login_required
def modify_user_info():
    form_info = ModifyUserInfoForm()
    form_password = ModifyUserPasswordForm()
    if form_info.validate_on_submit():
        master_user = MasterUser.query.get(current_user.id)
        if master_user is not None and master_user.verify_password(form_info.password.data):
            master_user.email = form_info.email.data
            db.session.add(master_user)
            db.session.commit()
            flash('信息修改成功。', 'success')
            return redirect(url_for('master.welcome'))

    return render_template('master/modify_user_info.html', form_password=form_password, form_info=form_info)


@master_blueprint.route('/modify_user_password', methods=['POST'])
@login_required
def modify_user_password():
    form_info = ModifyUserInfoForm()
    form_password = ModifyUserPasswordForm()

    if form_password.validate_on_submit():
        master_user = MasterUser.query.get(current_user.id)
        if master_user is not None and master_user.verify_password(form_password.old_password.data):
            master_user.password = form_password.new_password.data
            db.session.add(master_user)
            db.session.commit()
            flash('密码修改成功。', 'success')
            return redirect(url_for('master.welcome'))

        flash('原密码错误。', 'form_password')

    return render_template('master/modify_user_info.html', form_password=form_password, form_info=form_info)


@master_blueprint.route('/user_list')
@login_required
def user_list():
    page = request.args.get('page', 1, type=int)
    limit = 20
    paginate = MasterUser.query.filter(MasterUser.username != 'webmaster').order_by(MasterUser.id.desc()).paginate(page, per_page=limit, error_out=False)
    print(paginate)
    users = paginate.items

    return render_template('master/user_list.html', users=users, paginate=paginate);


@master_blueprint.route('/user_edit/<int:id>', methods=['PUT'])
@login_required
def user_delete(id):
    pass


@master_blueprint.route('/user_delete/<int:id>', methods=['DELETE'])
@login_required
def user_delete(id):
    pass
