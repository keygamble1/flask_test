from datetime import datetime
from flask import Blueprint, flash, g, redirect,render_template, request, url_for

from pybo.forms import AnswerForm, QuestionForm
from pybo.models import Answer, Question, User
from pybo.views.auth_views import login, login_required
from .. import db

bp=Blueprint('question',__name__,url_prefix='/question')

# 환경을 설정을 안했기때문에 ctrl+shift+p로 계속 가상환경을 불러오면서 해야한다
@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    
    form = QuestionForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(),user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)

@bp.route('/list/')
def _list():
    # main.index에서 처음부터 url_for가되어있기때문에 안함
    page=request.args.get('page',type=int,default=1)
    
    
    kw=request.args.get('kw',type=str,default='')
    question_list = Question.query.order_by(Question.create_date.desc())
    if kw:
        search='%%{}%%'.format(kw)
        sub_query=db.session.query(Answer.question_id,Answer.content,User.username) \
            .join(User,Answer.user_id ==User.id).subquery()
            # 엑세스 쿼리 떠올리며넛 하기
        question_list=question_list \
            .join(User) \
            .outerjoin(sub_query,sub_query.c.question_id==Question.id) \
            .filter(Question.subject.ilike(search) |
                    Question.content.ilike(search) |
                    User.username.ilike(search) |
                    sub_query.c.content.ilike(search) |
                    sub_query.c.username.ilike(search)
                    )\
                .distinct()
  
        
    
    
    question_list=question_list.paginate(page=page,per_page=10)
 
    # question_list=이제 list/?page=5 이런식으로나오며 객체전달해서 method상가능
    return render_template('question/question_list.html', question_list=question_list,page=page,kw=kw)

@bp.route('/detail/<int:question_id>')
def detail(question_id):
    form=AnswerForm()
    question=Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html',question=question,form=form)

@bp.route('/modify/<int:question_id>',methods=('GET','POST'))
@login_required
def modify(question_id):
    question=Question.query.get_or_404(question_id)
    if g.user !=question.user:
        flash('수정권한x')
        return redirect(url_for('question.detail',question_id=question_id))
    if request.method == 'POST':
        form =QuestionForm()
        
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date=datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail',question_id=question_id))
    else:
        form=QuestionForm(obj=question)
    return render_template('question/question_form.html',form=form)

# 객체를 전달해 속성을 전달하는역할이지 context는 값을 전달하는거랑 무관
@bp.route('/delete/<int:question_id>')
@login_required
# 무조건 어노테이션 넣어햐함 @bp에도
def delete(question_id):
    question=Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한 x')
        return redirect(url_for('question.detail',question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    # redirect할떄 넘겨줄게있으면 쓰고 아니면 말고 view에 들어가는거니까
    return redirect(url_for('question._list'))


# url_for는 view를 넣는것 quesiton.xx answer.xx이거다 view임
@bp.route('/vote/<int:question_id>/')
@login_required
def vote(question_id):
    _question=Question.query.get_or_404(question_id)
    if g.user ==_question.user:
        flash('본인작성x')
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))