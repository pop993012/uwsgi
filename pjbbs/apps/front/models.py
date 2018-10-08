from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
import shortuuid
from enum import Enum

class GenderEnum(Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOW = 4

class Froneuser(db.Model):
    __tablename__='frontuser'
    id=db.Column(db.String(100),primary_key=True,default=shortuuid.uuid)
    telephone = db.Column(db.String(11), nullable=False, unique=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    _password = db.Column(db.String(200), nullable=False)  # 加密过的
    email = db.Column(db.String(30), unique=True)
    realname = db.Column(db.String(50))
    avatar = db.Column(db.String(100))  # 头像
    signature = db.Column(db.String(100))  # 签名
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.UNKNOW)
    join_time = db.Column(db.DateTime, default=datetime.now)
    def __init__(self,password,**kwargs):
        self.password = password
        kwargs.pop('password',None)
        super(Froneuser,self).__init__(**kwargs)
    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, frontpwd):
        self._password = generate_password_hash(frontpwd)
    def checkpwd(self, frontpwd):
        # return self.password == generate_password_hash(frontpwd)
        return check_password_hash(self._password, frontpwd)