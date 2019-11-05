# coding: UTF-8
import os
import uuid


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
