from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField
from wtforms.validators import Email,InputRequired,Length,Regexp,EqualTo
from apps.common.checkaa import *
from wtforms.validators import ValidationError
from apps.front.models import *
from apps.common.models import *

class BaseForm(FlaskForm):
    @property    # 把函数变成了属性来调用
    def err(self):
        return self.errors.popitem()[1][0]


class Cphone(BaseForm):
    telephone=StringField(validators=[InputRequired(message='不能为空'),Regexp('^1[35786]\d{9}$',message='请输入正确的手机号')])

class checkall(Cphone):
    smscode=StringField(validators=[InputRequired(message='手机验证码不能为空')])
    username=StringField(validators=[InputRequired(message='用户名不能为空')])
    passwprd=StringField(validators=[InputRequired(message='密码不能为空')])
    password1=StringField(validators=[InputRequired(message='密码不能为空'),EqualTo('passwprd',message='两次密码不一致')])
    captchacode=StringField(InputRequired(message='验证码不能为空'))
    def validate_smscode(self,filed):
        smscode=getCode(self.telephone.data)
        print(smscode)
        if smscode.upper() != filed.data:

            raise ValidationError('SJ验证码不正确')
        if not smscode:
            raise  ValidationError('SJ请获取验证码')
    def validate_username(self,filed):
        r=Froneuser.query.filter(Froneuser.username == filed.data).first()
        if r:
            raise  ValidationError('用户名已存在')
    def validate_captchacode(self,filed):
        r = getCode(filed.data)
        if not r:
            raise ValidationError('1验证码不正确')


class checkUsername(BaseForm):
    telephone=StringField(validators=[InputRequired(message='不能为空'),Regexp('^1[35786]\d{9}$',message='请输入正确的手机号')])
    password = StringField(validators=[InputRequired(message='密码不能为空')])
    def validate_telephone(self,filed):
        r=Froneuser.query.filter(Froneuser.telephone == filed.data).first()
        print(r)
        if not r:
            raise  ValidationError('手机号不存在请注册')

class CZ(checkUsername):
    code=StringField(validators=[InputRequired(message='手机验证码不能为空')])
    def validate_code(self,filed):
        smscode=getCode(self.telephone.data)
        print(smscode)
        if smscode.upper() != filed.data:

            raise ValidationError('SJ验证码不正确')
        if not smscode:
            raise  ValidationError('SJ请获取验证码')

class addPost(BaseForm):
    title=StringField(validators=[InputRequired(message='不能为空')])
    boarder_id=IntegerField(validators=[InputRequired(message='板块不能为空')])
    content=StringField(validators=[InputRequired(message='不能为空')])
    # def validate_boarder_id(self,filed):
    #     #     r=AddPost.query.filter(AddPost.board_id==filed.data).first()
    #     #     if not  r:
    #     #         raise ValidationError('板块不正确')

