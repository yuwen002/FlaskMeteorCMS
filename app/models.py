# coding: UTF-8
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


# 用户类
class MasterUser(db.Model, UserMixin):
    """后台用户"""
    __tablename__ = 'master_users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    role_id = db.Column(db.SmallInteger, db.ForeignKey("master_roles.id"), default=0, comment='用户角色')
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    login_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<%s (%r)>' % (self.__class__.__name__, self.username)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


roles_permissions = db.Table(
    'roles_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('master_roles.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('master_permission.id'))
)


# 用户角色
class Role(db.Model):
    """用户角色"""
    __tablename__ = 'master_roles'
    id = db.Column(db.Integer, primary_key=True, comment='自增ID')
    name = db.Column(db.String(20), unique=True, nullable=False)
    remark = db.Column(db.String(200))
    users = db.relationship('MasterUser', backref='roles', lazy='dynamic')
    roles_to_permissions = db.relationship('Permission', secondary=roles_permissions, backref='permissions_to_roles', lazy='dynamic')


# 权限数据
class Permission(db.Model):
    __tablename__ = 'master_permission'
    id = db.Column(db.Integer, primary_key=True, comment='自增ID')
    name = db.Column(db.String(20), unique=True)
    remark = db.Column(db.String(200), comment='权限名称备注')


# 单页数据
class SingePage(db.Model):
    __tablename__ = 'single_pages'
    id = db.Column(db.Integer, primary_key=True, comment='自增ID')
    single_category_id = db.Column(db.Integer, db.ForeignKey('single_category.id'), default=0, comment='单页数据分类ID')
    title = db.Column(db.String(64), comment='单页文章标题')
    content = db.Column(db.Text, comment='单页内容')
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())


# 单页数据分类
class SingleCategory(db.Model):
    __tablename__ = 'single_category'
    id = db.Column(db.Integer, primary_key=True, comment='自增ID')
    name = db.Column(db.String(32), unique=True, comment='分类名称')
    description = db.Column(db.String(128), comment='分类描述')
    img = db.Column(db.String(200), comment='分类图片')
    singlepages = db.relationship('SingePage', backref='single_categorys')


# 新闻分类
class ArticleCategory(db.Model):
    """
    新闻分类表
    左右无限分类
    """
    __tablename__ = 'article_category'
    id = db.Column(db.Integer, primary_key=True)
    fid = db.Column(db.Integer, default=0)
    name = db.Column(db.String(32), unique=True)
    img = db.Column(db.String(200), comment='分类图片')
    lft = db.Column(db.Integer, default=0)
    rgt = db.Column(db.Integer, default=0)
    sort = db.Column(db.Integer, default=0)
    status = db.Column(db.SmallInteger, default=0)
    depth = db.Column(db.SmallInteger, default=0)
    input_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())
    # news = db.relationship()

    def __repr__(self):
        return "<Category %r>" % self.name

    def get_category(self, id):
        category = ArticleCategory.query.get(id)
        return category

    def add_category(self, name, fid=0, sort=0, img=''):
        if int(fid) == 0:
            # 查询左值最小值如最小值为空进行顶级分类写入
            left = db.session.query(func.min(ArticleCategory.lft)).scalar()
            if left is None:
                category = ArticleCategory(name=name, depth=0, lft=1, rgt=2, img=img)
                db.session.add(category)
                db.session.commit()
                return True
            else:
                return None
        else:
            # 获取父类分类基本信息
            category = self.get_category(fid)
            if category is not None:
                # 其它节点分类信息更新
                new_category = ArticleCategory(name=name, fid=fid, depth=category.depth + 1, lft=category.rgt, rgt=category.rgt + 1, sort=sort, img=img)
                db.session.query(ArticleCategory).filter(ArticleCategory.lft > category.rgt).update({ArticleCategory.lft: ArticleCategory.lft + 2})
                db.session.query(ArticleCategory).filter(ArticleCategory.rgt >= category.rgt).update({ArticleCategory.rgt: ArticleCategory.rgt + 2})
                db.session.add(new_category)
                db.session.commit()
                return True
            else:
                return None

    def delete_category(self, id):
        category = self.get_category(id)
        # 删除传入ID信息，并删除子分类
        ArticleCategory.query.filter(ArticleCategory.lft >= category.lft, ArticleCategory.rgt <= ArticleCategory.rgt).delete()
        # 更新受影响的左右树
        value = category.rgt - category.lft + 1
        ArticleCategory.query.filter(ArticleCategory.lft > category.lft).update({ArticleCategory.lft: ArticleCategory.lft - value})
        ArticleCategory.query.filter(ArticleCategory.rgt > category.rgt).update({ArticleCategory.rgt: ArticleCategory.rgt - value})

        db.session.commit()

    def get_category_all(self):
        return ArticleCategory.query.order_by(ArticleCategory.lft).all()


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, comment='自增ID')
    category_id = db.Column(db.Integer, db.ForeignKey('article_category.id'), default=0, comment='关联分类ID')
    external_links = db.Column(db.String(300), default=None, comment='文章外链')
    title = db.Column(db.String(64), nullable=False, comment='文章标题')
    short_title = db.Column(db.String(32), comment='文章短标题')
    synopsis = db.Column(db.String(64), comment='文章简介')
    author = db.Column(db.String(10), comment='文章作者')
    article_date = db.Column(db.DateTime, default=datetime.now(), comment='文章日期')
    sort = db.Column(db.Integer, comment='文章排序')
    recommend = db.Column(db.String(20), comment='文章推荐')
    tag = db.Column(db.String(80), comment='TAG标签')
    source = db.Column(db.String(24), comment='文章来源')
    img = db.Column(db.String(200), comment='文章图片')
    content = db.Column(db.Text, comment='文章内容')
    status = db.Column(db.SmallInteger, comment='文章状态')
    comment_on_status = db.Column(db.Boolean, default=True, comment='文章评论状态')

    seo_title = db.Column(db.String(100), comment='SEO标题')
    seo_keyword = db.Column(db.String(150), comment='SEO关键字')
    seo_description = db.Column(db.String(200), comment='SEO描述')

    created_at = db.Column(db.DateTime, default=datetime.now(), comment='写入时间')
    updated_at = db.Column(db.DateTime, default=datetime.now(), comment='最后更新时间')
