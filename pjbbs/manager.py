# flask_script 使用命令行管理项目
from flask_script import Manager
# flask_migrate 数据库迁移脚本
from flask_migrate import Migrate,MigrateCommand
from apps.common.models import *
from pjjk import app
from exts import db

from apps.cms.models import User,Roel,cms_role_user
from apps.front.models import *

# flask-script的使用
manage = Manager(app)
# 要使用flask-migrate必须绑定app和db
Migrate(app,db)
# 把MigrateCommand(数据库迁移)命令添加到manager
manage.add_command("db",MigrateCommand)

@manage.option('-e','--email',dest='email')
@manage.option('-u','--username',dest='username')
@manage.option('-p','--password',dest='password')
def addcmsuser(email,username,password):
    user = User(email=email,username=username,password=password)
    db.session.add(user)
    db.session.commit()

@manage.option('-r','--roelname',dest='roelname')
@manage.option('-d','--desc',dest='desc')
@manage.option('-p','--permissions',dest='permissions')
def addcmsusera(roelname,desc,permissions):
    roel = Roel(roelname=roelname,desc=desc,permissions=permissions)
    db.session.add(roel)
    db.session.commit()

@manage.option('-u','--uid',dest='uid')
@manage.option('-r','--rid',dest='rid')
def addcmsuserb(uid,rid):
    u = User.query.get(uid)
    r = Roel.query.get(rid)
    u.roles.append(r)
    db.session.commit()

@manage.command
def addpost():
    for i  in range(100):
        post=AddPost(title="title"+str(i),content="content"+str(i),board_id=1,user_id="zvqTLWJsM5oiQ9Yv6ZiQeb")
        db.session.add(post)
        db.session.commit()
    print('ok')


if __name__ == '__main__':
    manage.run()


