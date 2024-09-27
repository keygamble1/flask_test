
import functools
from flask import Blueprint, g, session, url_for, render_template, flash, request
from werkzeug.security import *
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')
@bp.route('/signup/',methods=('GET','POST'))
# bp.route로 __init__에서 쓸수있음 register로
def signup():
   form=UserCreateForm()
   if request.method=="POST" and form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if not user:
                user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
                db.session.add(user)
                db.session.commit()
                
                return redirect(url_for('main.index'))
        else:
                flash('이미 존재함')
                # tempete은 html
   return render_template('auth/signup.html',form=form)

@bp.route('/login/',methods=('GET','POST'))
def login():
        form=UserLoginForm()
        if request.method=='POST' and form.validate_on_submit():
                error=None
                user=User.query.filter_by(username=form.username.data).first()
                if not user:
                        error='존재안함'
                elif not check_password_hash(user.password,form.password.data):
                        error='비밀번호 올바르지않음'
                # model과 form을 각각 비교함
                # model은 db,form은 유효성검사하는 객체이기때문에 반드시 일치해야함
                if error is None:
                   session.clear()
                #    세션은 서버에 브라우저에 보내기위한 별도의 메모리
                # 브라우저가 서버에 요청보낼시 REQUEST는 객체를 새로만들지만
                # SESSION(서버) 는 계속만드는게아닌 이미 저장된 메모리를 보낸다
                # 이미 저장되어있는 세션을 URL에서 읽는거라고보면되고
                # 처음에는 브라우저 REQUEST->서버응답으로 하는데
                # 서버응답완료시 연결끊어짐
                # 하지만 세션 메모리는 남아있기때문에 
                # 다시연결시 서버(세션메모리)는 동일해짐
                # 서버가 처음 브라우저에 보낼때는 쿠키를 보내는데,
                # 이때 브라우저는 받은 쿠키+HTTP조합 +URL로 다시 서버에보낸다
                # 그럼 서버는 저장된 세션을 보내버림 
                # 이때 세션은 쿠키 1개당 생성되는 메모리 공간이라보자
                   session['user_id']=user.id
                   _next=request.args.get('next','')
                   if _next:
                           return redirect(_next)
                   else:
                         
                        return redirect(url_for('main.index'))
                flash(error)
        return render_template('auth/login.html',form=form)

@bp.before_app_request
def load_login_in_user():
        user_id=session.get('user_id')
        if user_id is None:
                g.user=None
        else:
                g.user=User.query.get(user_id)

@bp.route('/logout/')
def logout():
        session.clear()
        return redirect(url_for('main.index'))

def login_required(view):
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
                if g.user is None:
                        _next=request.url if request.method=='GET' else ''
                        return redirect(url_for('auth.login',next=_next))
                return view(*args, **kwargs)
        
        return wrapped_view