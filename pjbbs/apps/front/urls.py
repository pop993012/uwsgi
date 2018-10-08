from flask import Blueprint,request,jsonify,make_response,session,redirect,url_for
from flask import render_template
from flask.views import MethodView
from apps.front.forms import *
from apps.common.baseResp import *
from dysms_python.demo_sms_send import  send_sms
import string,random,json
from apps.common.captcha.xtcaptcha import Captcha
from io import BytesIO
from apps.common.models import *
from apps.common.checkaa import *
from  apps.front.models import *
from config import *

from functools import *
from task import SendSMS
from flask_paginate import *
bp = Blueprint('front',__name__)
def lonigDecotor(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if not session.get(FRONT_USER_ID,None):
            return redirect(location=url_for("front.signin"))
        else:
            r = func(*args,**kwargs)
            return r
    return inner



@bp.route("/")
@lonigDecotor
def loginView():
    a=request.args.get('a')
    print('ok')
    print(session[FRONT_USER_ID])
    page=request.args.get(get_page_parameter(), type=int, default=1)
    begin = (page - 1) * 10
    end = begin + 10
    border_id=request.args.get('boarder_id')
    print(border_id)
    if border_id:
        posts=AddPost.query.filter(AddPost.board_id==border_id).slice(begin,end)
        count = AddPost.query.filter(AddPost.board_id == border_id).count()
        print(posts)
    else:
        posts=AddPost.query.slice(begin,end)
        count=AddPost.query.count()
    if a:
        posts = AddPost.query.outerjoin(Tag, AddPost.id == Tag.post_id).order_by(Tag.create_time.desc()).slice(begin,end)

    banners = LBT.query.order_by(LBT.priority.desc()).limit(4)
    bk=BK.query.all()
    user_id=session[FRONT_USER_ID]
    r=Froneuser.query.filter(Froneuser.id==user_id).first()
    pagination=Pagination(bs_version=3,page=page, total=count)
    context = {
        'banners': banners,
        'bks':bk,
        'posts':posts,
        'username':r.username,
        'page':page,
        'pagination':pagination
    }
    return render_template("front/index.html", **context)




class Sigup(MethodView):
    def get(self):
        return  render_template('front/singUp.html')
    def post(self):
        fm =checkall(formdata=request.form)
        if fm.validate():
            r=Froneuser(username=fm.username.data,password=fm.passwprd.data,
                        telephone=fm.telephone.data)
            db.session.add(r)
            db.session.commit()
            delete(fm.telephone.data)
            delete(fm.captchacode.data)
            return jsonify(respSuccess(msg='成功了'))
        else:
            return jsonify(respParamErr(msg=fm.err))
bp.add_url_rule('/sigup/',endpoint='signup',view_func=Sigup.as_view('signup'))

class SigIN(MethodView):
    def get(self):
        local=request.headers.get('Referer')
        if not local:
            local='/'
        context={
            'local':local
        }
        return render_template('front/singIN.html',**context)
    def post(self):
        fm=checkUsername(formdata=request.form)
        print(111)
        if fm.validate():
            user=Froneuser.query.filter(Froneuser.telephone==fm.telephone.data).first()
            a=user
            user=user.checkpwd(fm.password.data)
            if user:
                 session[FRONT_USER_ID]=a.id
                 return jsonify(respSuccess(msg='成功'))
            else:
                return jsonify(respParamErr(msg='密码错误'))
        else:
            return jsonify(respParamErr(msg=fm.err))
bp.add_url_rule('/sigin/',endpoint='signin',view_func=SigIN.as_view('signin'))

class CZpassword(MethodView):
    def get(self):
        return render_template('front/regisr.html')
    def post(self):
       fm=CZ(formdata=request.form)
       if fm.validate():
           user=Froneuser.query.filter(Froneuser.telephone==fm.telephone.data).first()
           if user:
               user.password =fm.password.data
               db.session.commit()
               return jsonify(respSuccess(msg='成功'))
           else:
               return  jsonify(respParamErr(msg='失败'))
       else:
           return jsonify(respParamErr(msg=fm.err))


bp.add_url_rule('/regist/',endpoint='regist',view_func=CZpassword.as_view('regist'))

@bp.route('/code/',methods=['post'])
def  zhale():
    fm=Cphone(formdata=request.form)
    if fm.validate():
        r = string.digits
        r=''.join(random.sample(r,4))
        saveCode(fm.telephone.data,r)
        print(r)
        r = SendSMS.delay(a1=fm.telephone.data,a2=r)
        print(1111111111)
        print(r)
        # if json.loads(r.decode("utf-8"))['Code'] == 'OK':
        return jsonify(respSuccess("短信验证码发送成功，请查收"))
        # else:  # 发送失败
        #     return jsonify(respParamErr("请检查网络"))

    else:
         return jsonify(respParamErr(msg=fm.err))

@bp.route('/send_imgcode/')
def ima_code():
    text,img=Captcha.gene_code()
    out=BytesIO()
    img.save(out,'png')
    out.seek(0)
    saveCode(text,text)
    print(text)
    reso=make_response(out.read())
    reso.content_type = "image/png"
    return reso

class  TZFB(MethodView):
    decorators = [lonigDecotor]
    def get(self):
        bks = BK.query.all()
        context={
            'BKS':bks
        }
        return  render_template('front/TZFB.html',**context)
    def post(self):
        fm=addPost(foamdata=request.form)
        if fm.validate():
            user_id=session[FRONT_USER_ID]
            r=AddPost(title=fm.title.data,content=fm.content.data,
                 board_id=fm.boarder_id.data,user_id=user_id)
            db.session.add(r)
            db.session.commit()
            return jsonify(respSuccess("已经成功"))
        else:
            return  jsonify(respParamErr(msg=fm.err))
@bp.route('/showpost/')
def showPost():
    post_id=request.args.get('post_id')
    print(post_id)
    post=AddPost.query.filter(AddPost.id==post_id).first()
    print(post)
    commons=Aaddcommon.query.order_by(Aaddcommon.create_time.desc()).all()
    context={
        'posts':post,
        'commons':commons
    }
    return render_template('front/showpost.html',**context)

@bp.route('/addcomm/',methods=['post'])
def addcommm():
    user_id=session[FRONT_USER_ID]
    print(user_id)
    if not user_id:
        return  jsonify(respParamErr(msg='你还没登录'))
    post_id=request.values.get('post_id')
    content=request.values.get('content')
    print(content)
    if content=='':
        return jsonify(respParamErr(msg='内容不能为空'))
    r=Aaddcommon(content=content,post_id=post_id,user_id=user_id)
    db.session.add(r)
    db.session.commit()
    return jsonify(respSuccess("已经成功"))



bp.add_url_rule('/tzfb/',endpoint='tzfb',view_func=TZFB.as_view('tzfb'))
