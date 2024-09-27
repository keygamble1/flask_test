from datetime import datetime

from flask import Blueprint, flash, g, render_template, request, url_for
from pybo import db

from pybo.forms import AnswerForm
from pybo.models import Answer, Question
from pybo.views.auth_views import login_required
from werkzeug.utils import redirect

bp = Blueprint('answer', __name__, url_prefix='/answer')



@bp.route('/create/<int:question_id>', methods=('POST',))
@login_required
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form['content']
        answer = Answer(content=content, create_date=datetime.now(),user=g.user)
        question.answer_set.append(answer)
        db.session.commit()
        return redirect(
        '#{}answer{}'.format(
            url_for('question.detail',question_id=question_id)
        ,answer.id)
            )
    return render_template('question/question_detail.html', question=question,form=form)

@bp.route('/modify/<int:answer_id>',methods={'GET','POST'})
@login_required
def modify(answer_id):
    answer=Answer.query.get_or_404(answer_id)
    if g.user !=answer.user:
        flash('수정x')
        return redirect(url_for('question.detail',question_id=answer.question.id))
    if request.method=='POST':
        form=AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            # 여기에서의 form은 html의 form이랑 엮으면안되고 
            # 논리적으로 form임 이걸자꾸 이미지화시켜서 html 자동반영된다고 생각x
            
            answer.modify_date=datetime.now()
            db.session.commit()
            return redirect(
                 '#{}answer{}'.format(
                url_for('question.detail',question_id=answer.question.id)
                ,answer.id)
                )
    else:
        form=AnswerForm(obj=answer)
            # kwrags에서 obj=None일거임
    return render_template('answer/answer_form.html',form=form)
@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer=Answer.query.get_or_404(answer_id)
    question_id=answer.question.id
    if g.user != answer.user:
        flash('삭제x')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(
         '#{}answer{}'.format(
        url_for('question.detail',question_id=question_id)
        ,answer.id)
        )
# url이 로딩되고 그담에 페이지
# 이순서가지금 url부터하는거
# url->views->html
# post만날시 html->url->views 이런식으로myproject/pybo/views/answer_views.py
@bp.route('/vote/<int:answer_id>/')
@login_required
def vote(answer_id):
    _answer=Answer.query.get_or_404(answer_id)
    if g.user == _answer.user:
        flash('본인x')
    else:
        _answer.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail',question_id=_answer.question.id))