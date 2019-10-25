# coding: UTF-8
from flask import render_template
from app.webmaster import master_blueprint


@master_blueprint.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@master_blueprint.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500
