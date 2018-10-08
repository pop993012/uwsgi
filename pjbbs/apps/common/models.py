from  exts import db
from datetime import datetime
import shortuuid

class LBT(db.Model):
    __tablename__='lbt'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    bannerName = db.Column(db.String(20), nullable=False)
    imglink = db.Column(db.String(200), nullable=False, unique=True)
    link = db.Column(db.String(200), nullable=False, unique=True)
    priority = db.Column(db.Integer, default=1)

class BK(db.Model):
    __tablename__='bk'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bkname=db.Column(db.String(20), nullable=False)
    bknum=db.Column(db.Integer,default=0)
    create_time=db.Column(db.DateTime,default=datetime.now)

class AddPost(db.Model):
    __tablename__ = "common_post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    board_id = db.Column(db.Integer, db.ForeignKey('bk.id'))
    board = db.relationship('BK', backref='posts')
    user_id = db.Column(db.String(100), db.ForeignKey('frontuser.id'), default=shortuuid.uuid)
    user = db.relationship('Froneuser', backref='posts')  # orm查询的时候使用

class Aaddcommon(db.Model):
    __tablename__ = "common_common"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.String(100), db.ForeignKey('frontuser.id'), default=shortuuid.uuid)
    user = db.relationship('Froneuser', backref='postsa')
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('common_post.id'))
    post = db.relationship('AddPost', backref='commons')

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('common_post.id'))
    post = db.relationship('AddPost', backref=db.backref('tag',uselist=False))
    status = db.Column(db.Boolean,default=False)
    create_time = db.Column(db.DateTime, default=datetime.now)