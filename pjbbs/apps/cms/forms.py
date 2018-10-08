# 进行表单校验
from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField
from wtforms.validators import Email,InputRequired,Length,URL
from apps.common.models import LBT,BK
from wtforms.validators import ValidationError

class BaseForm(FlaskForm):
    @property    # 把函数变成了属性来调用
    def err(self):
        return self.errors.popitem()[1][0]


class UserForm(BaseForm):
    email = StringField(validators=[Email(message="必须为邮箱"),InputRequired(message="不能为空")])
    password = StringField(validators=[InputRequired(message="必须输入密码"),Length(min=6,max=40,message="密码长度是6-40位")])


class Updatepwd(BaseForm):
    oldpwd = StringField(validators=[InputRequired(message="必须输入密码"), Length(min=6, max=40, message="密码长度是6-40位")])
    pwd = StringField(validators=[InputRequired(message="必须输入密码"), Length(min=6, max=40, message="密码长度是6-40位")])
    pwd2=StringField(validators=[InputRequired(message="必须输入密码"), Length(min=6, max=40, message="密码长度是6-40位")])

class  email1(BaseForm):
    email = StringField(validators=[Email(message="必须为邮箱"), InputRequired(message="不能为空")])



class  email2(BaseForm):
    email = StringField(validators=[Email(message="必须为邮箱"), InputRequired(message="不能为空")])


class addlbt(BaseForm):
    bannerName=StringField(validators=[InputRequired(message='不能为空')])
    imglink = StringField(validators=[InputRequired(message="不能为空"), URL(message="必须是一个url地址")])
    link = StringField(validators=[InputRequired(message="不能为空"), URL(message="必须是一个url地址")])
    priority = IntegerField(validators=[InputRequired(message='必须输入优先级')])

    def validate_imglink(self, filed):
        r = LBT.query.filter(LBT.imglink == filed.data).first()
        if r:
            raise ValidationError('图片的url已存在，请勿重复添加 ' + str(r.id) + r.bannerName)

    def validate_link(self, filed):
        r = LBT.query.filter(LBT.link == filed.data).first()
        if r:
            raise ValidationError('内容的url已存在，请勿重复添加 ' + str(r.id) + r.bannerName)
class UPdate(addlbt):
    id=StringField(validators=[InputRequired(message='不能为空')])

    def validate_imglink(self, filed):
        pass

    def validate_link(self, filed):
        pass


class addBK(BaseForm):
    bkname=StringField(validators=[InputRequired(message='不能为空')])
    def validate_bkname(self, filed):
        r=BK.query.filter(BK.bkname==filed.data).first()
        if r:
            raise ValidationError('所添加板块已经存在')