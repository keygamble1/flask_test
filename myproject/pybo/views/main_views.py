from flask import Blueprint, redirect, render_template, url_for
from pybo.models import Question

bp=Blueprint('main',__name__,url_prefix='/')

@bp.route('/hello')
def hello_pybo():
    return "hello,pybo"

@bp.route('/')
def index():
    return redirect(url_for('question._list'))

    # django에서는 url.py에서 name으로 렌더링해서 알아서 찾아갔지만
    # 여기서는 context로 묶어줘야함
    