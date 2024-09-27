from venv import create
from pybo.models import Question,Answer
from datetime import datetime
q=Question(subject='pybo가뭔가?',content='pybo에대해알고싶음',create_date=datetime.now())

from pybo import db
db.session.add(q)
db.session.commit()

q=Question(subject='플라스크모델',content='id는 자동생성?',create_date=datetime.now())
db.session.add(q)
db.session.commit()
# 저장삭제 작업후 반드시,commit해서 데이터에 저장 save아님
Question.query.all()
Question.query.filter(Question.id==1).all()
Question.query.filter(Question.subject.like('%플라스크%')).all()
q=Question.query.get(2)
a=Answer(question=q,content='자동생성',create_date=datetime.now())
db.session.add(a)
db.session.commit()