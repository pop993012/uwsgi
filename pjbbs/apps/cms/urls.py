# 后台
from flask import Blueprint,session
from flask import render_template
from apps.cms.forms import *
from flask import request,jsonify
from apps.common.baseResp import *
from exts import db,mail
from apps.cms.models import *
from config import CURRENT_USER_ID,CURRENT_USER,REMBERME
from flask.views import MethodView
import string
from flask_mail import Message
import random
from apps.common.checkaa import *
from apps.common.models import *
from functools import wraps
from qiniu import Auth
bp = Blueprint('cms',__name__,url_prefix="/cms")


@bp.route("/qiniu_token/")
def qiniukey():
    # 通过secer-key id 生成一个令牌，返回给客户端
    ak = "gixRZTC9nnM_ODSEyAmDtFPVBD5sBWJo1dsfszvB"
    sk = "X8TYRWzELi-hfyzl1MeAkEbS9i5DKL_8qI4m_o3l"
    q = Auth(ak, sk)
    bucket_name = 'pjssb' # 仓库的名字
    token = q.upload_token(bucket_name)
    return jsonify({'uptoken': token})



def checkPer(per):
    def outer(f):
        @wraps(f)
        def inner(*args,**kwargs):
            userid=session.get(CURRENT_USER_ID)
            user = User.query.get(userid)
            r = user.checkpermission(per)
            if r:
                return f(*args, **kwargs)
            else:
                return render_template("cms/login.html")
        return inner
    return outer



@bp.route("/")
def loginView():
    return render_template("cms/login.html")

@bp.route('/login/',methods=['post'])
def login():
    fm = UserForm(formdata=request.form)
    if fm.validate():
        email = fm.email.data # name=email的值
        pwd = fm.password.data
        user = User.query.filter(User.email == email).first()
        if not user : # 没有查询到用户
            return jsonify(respParamErr('用户名不对'))
        #if user.password == pwd : # 登陆成功
        if user.checkPwd(pwd):
            rem=request.values.get('rem')
            print(rem)
            session[CURRENT_USER_ID]=user.id
            session[REMBERME]=123
            if rem == '1':  # 前端勾选了记住我
                print(333)
                session.permanent = True  # 设置这个属性之后回去config访问过期天数，如果没有设置，默认是31天
            return jsonify(respSuccess('登陆成功'))
        else: # 密码错误
            return jsonify(respParamErr("密码错误"))
    else:
        return jsonify(respParamErr(msg=fm.err))
@bp.route('/index/')
def cms_index():
    return render_template('cms/cms_index.html')
@bp.context_processor
def aa():
    rem=session.get(REMBERME)
    if rem ==123:
        user_id =session[CURRENT_USER_ID]
        user = User.query.get(user_id)
        return {'user': user}
    return {}
@bp.route('/msg/')
def bb():
    return render_template('cms/msg.html')
@bp.route('/aa/')
def get1():
        return  render_template('cms/updatapwd.html')
@bp.route('/cc/',methods=['post'])
@checkPer(Permission.USER_INFO)
def post1():
        print('开始')
        fm=Updatepwd(formdata=request.form)
        if fm.validate():
           print('结束')
           used_id=session[CURRENT_USER_ID]
           user=User.query.get(used_id)
           r=user.checkPwd(fm.oldpwd.data)
           if r:
               user.password =fm.pwd.data
               db.session.commit()
               return jsonify(respSuccess(msg='修改成功'))
           else:
               return jsonify(respParamErr(msg='旧密码错误'))
        else:
            return jsonify(respParamErr(msg=fm.err))
class updateem(MethodView):
    decorators =[checkPer(Permission.USER_INFO)]
    def get(self):
        return render_template('cms/updateEmail.html')
    def post(self):
        fm=email2(formdata=request.form)
        user = User.query.filter(User.email == fm.email.data).first()
        if user:
            return jsonify(respParamErr(msg='邮箱已注册'))
        emailcode = getCode('fm.email.data')
        print(111)
        print(emailcode)
        print( request.form.get('emailcode').upper())
        if not emailcode or emailcode != request.form.get('emailcode').upper():

            return jsonify(respParamErr(msg='请输入正确的邮箱验证码'))
        user = User.query.get(session[CURRENT_USER_ID])
        user.email = fm.email.data
        db.session.commit()
        return jsonify(respSuccess(msg='修改邮箱成功'))
bp.add_url_rule('/ii/',endpoint='ii',view_func=updateem.as_view('ii'))



@bp.route('/oo/',methods=['post'])
@checkPer(Permission.USER_INFO)
def check():
    fm = email1(formdata=request.form)
    if fm.validate():
        user = User.query.filter(User.email == fm.email.data).first()
        if user:
            return jsonify(respParamErr(msg='邮箱已经存在'))
        else:
            res=string.ascii_letters+string.digits
            r = ''.join(random.sample(res, 6))
            saveCode('fm.email.data',r)
            msg = Message("更新邮箱验证码", recipients=[fm.email.data], body="验证码为" + r)
            mail.send(msg)
            return jsonify(respSuccess(msg='发送成功，请查看邮箱'))
    else:
        return jsonify(respParamErr(msg=fm.err))




@bp.route('/pp/')
@checkPer(Permission.BANNER)
def ppooopi():
    lbt= LBT.query.all()
    context = {
        'banners': lbt
    }
    return render_template("cms/lbt.html", **context)

    return render_template('cms/lbt.html')

@bp.route('/nb/',methods=['post'])
@checkPer(Permission.BANNER)
def addLOPOBT():
    fm=addlbt(formdata=request.form)
    if fm.validate():
        lbt=LBT(
            bannerName=fm.bannerName.data,
            imglink=fm.imglink.data,
            link=fm.link.data,
            priority=fm.priority.data

        )
        db.session.add(lbt)
        db.session.commit()
        return jsonify(respSuccess(msg='添加成功'))
    else:
        return jsonify(respParamErr(msg=fm.err))

@bp.route('/iop/',methods=['post'])
@checkPer(Permission.BANNER)
def yuiop():
    id=request.form.get('id')
    user=LBT.query.filter(LBT.id==id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(respSuccess(msg='删除成功'))
    else:
        return jsonify(respParamErr(msg='删除失败'))



@bp.route('/lb/',methods=['post'])
@checkPer(Permission.BANNER)
def yuiwwwop():
    fm=UPdate(formdata=request.form)
    if fm.validate():
        user=LBT.query.filter(LBT.id==id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify(respSuccess(msg='更新成功'))
        else:
            return jsonify(respParamErr(msg='更新失败'))
    else:
        return jsonify(respParamErr(msg=fm.err))
@bp.route('/BK/')
def BKA():
    bk = BK.query.all()
    context = {
        'bks': bk
    }
    return render_template('cms/BK.html',**context)



@bp.route('/nv/',methods=['post'])
def nv():
    fm=addBK(formdata=request.form)
    if fm.validate():
        bk=BK(bkname=fm.bkname.data)
        db.session.add(bk)
        db.session.commit()
        return jsonify(respSuccess(msg='添加成功'))
    else:
        return jsonify(respParamErr(msg='添加失败'))


@bp.route('/delbk/',methods=['post'])
def delnk():
    id=request.form.get('id')
    print('--*-*-*-*-*---')
    print(id)
    bk=BK.query.filter(BK.id==id).first()
    if bk:
        db.session.delete(bk)
        db.session.commit()
        return jsonify(respSuccess(msg='删除成功'))
    else:
         return jsonify(respParamErr(msg='删除失败'))



@bp.route('/updatebk/',methods=['post'])
def updatebk():
    fm = addBK(formdata=request.form)
    if fm.validate():
        bk = BK(bkname=fm.bkname.data)
        db.session.add(bk)
        db.session.commit()
        return jsonify(respSuccess(msg='更新成功'))
    else:
        return jsonify(respParamErr(msg='更新失败'))



@bp.route('/showpp/')
def  showPOST():
    r=AddPost.query.all()
    context={
        'posts':r
    }
    return render_template('cms/post.html',**context)


@bp.route('/addqwe/',methods=['post'])
def addqwe():
    post_id=request.values.get('post_id')
    print(post_id)
    r=AddPost.query.filter(AddPost.id ==post_id).first()
    if r:
        tag=Tag(post=r,status=True)
        db.session.add(tag)
        db.session.commit()
        return jsonify(respSuccess(msg='加精成功'))
    else:
        return jsonify(respParamErr(msg='加精失败'))




@bp.route('/deleteqwe/',methods=['post'])
def  deleteqwe():
    post_id = request.values.get('post_id')
    print('-*-*-*-*-')
    print(post_id)
    r = Tag.query.filter(Tag.post_id==post_id).first()
    if r:
        r.status=False
        db.session.commit()
        return jsonify(respSuccess(msg='取消成功'))
    else:
        return jsonify(respParamErr(msg='取消失败'))
