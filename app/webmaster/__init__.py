# coding: UTF-8
from flask import Blueprint

master_blueprint = Blueprint(
    'master',
    __name__,
    url_prefix='/master',
    template_folder='./templates',
)

from app.webmaster.controllers import master, errors
