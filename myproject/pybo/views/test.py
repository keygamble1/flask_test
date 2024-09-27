from re import sub
from pybo import db
from pybo.models import Question
from datetime import datetime

for i in range(300):
    q=Question(subject='테스트데이터[%03d]' %i,content='내용무',\
        create_date=datetime.now())
    db.session.add(q)
    db.session.commit()