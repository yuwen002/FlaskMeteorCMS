# coding: UTF-8
import os
import uuid
from datetime import datetime
from flask import current_app

# 文件重命名
def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


# 创建目录
def mkdir(path):
    is_exits = os.path.exists(path)

    if not is_exits:
        os.makedirs(path)
        return True

    return False


# 验证上传文件类型
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg', 'gif', 'txt']


# 上传文件路径建立，并重命名文件
def upload_mkdir(filename):
    """
    :param filename: 上传文件名
    :return 上传路径， 文件路径:
    """
    today_path = datetime.now().strftime("%Y%m%d")
    img_name = random_filename(filename)
    img_path = os.path.join(today_path, img_name).replace('\\', '/')
    upload_path = os.path.join(current_app.config['UPLOAD_PATH'], today_path)
    mkdir(upload_path)
    upload_path = os.path.join(upload_path, img_name)

    return upload_path, img_path
