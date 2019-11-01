# coding: UTF-8
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, login_required, logout_user, current_user
from app.webmaster import master_blueprint
from app.webmaster.forms.master import MasterLoginForm, RegisterUserForm, ModifyUserInfoForm, ModifyUserPasswordForm, ModifyRegUserInfoForm
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
        email = form.email.data.lower()

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


# 当前用户信息
@master_blueprint.route('/user_info')
@login_required
def user_info():
    form_info = ModifyUserInfoForm()
    form_password = ModifyUserPasswordForm()

    return render_template('master/modify_user_info.html', form_password=form_password, form_info=form_info)


# 更改当前用户信息
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


# 更改当前用户密码
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


# 用户信息列表
@master_blueprint.route('/user_list')
@login_required
def user_list():
    page = request.args.get('page', 1, type=int)
    limit = 2
    paginate = MasterUser.query.filter(MasterUser.username != 'webmaster').order_by(MasterUser.id.desc()).paginate(page, per_page=limit, error_out=False)
    users = paginate.items
    session['user_list_path'] = request.full_path
    return render_template('master/user_list.html', users=users, paginate=paginate);


@master_blueprint.route('/user_edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_edit(user_id):
    user = MasterUser.query.get_or_404(user_id)
    # form初始化
    form = ModifyRegUserInfoForm()

    if form.validate_on_submit():
        u_info = MasterUser.query.filter(MasterUser.email == form.email.data, MasterUser.id != user_id).first()

        if u_info is None:
            user.email = form.email.data
            if form.password.data:
                user.password = form.password.data

            db.session.commit()

            path = session.get('user_list_path')
            if path:
                endpoint = path
            else:
                endpoint = url_for('master.user_list')

            return redirect(endpoint)
        else:
            flash('邮箱已存在')

    #input value赋值
    form.email.data = user.email
    form.username.data = user.username

    return render_template('master/user_edit.html', user_id=user_id, form=form)


# 删除用户信息
@master_blueprint.route('/user_delete/<int:user_id>', methods=['GET'])
@login_required
def user_delete(user_id):
    user = MasterUser.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('master.user_list'))
