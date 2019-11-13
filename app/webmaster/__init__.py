# coding: UTF-8
from flask import Blueprint

master_blueprint = Blueprint(
    'master',
    __name__,
    url_prefix='/master',
    template_folder='./templates',
)

singlepage_blueprint = Blueprint(
    'singlepage',
    __name__,
    url_prefix='/master/singlepage',
    template_folder='./templates'
)

article_blueprint = Blueprint(
    'article',
    __name__,
    url_prefix='/master/article',
    template_folder='./templates'
)

from app.webmaster.controllers import (
    master,
    singlepage,
    article,
    errors
)
