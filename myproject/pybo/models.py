from http import server
# This line of code is defining a foreign key relationship in the `Question` table.
from pybo import db

# import sqlalchemy as db
# model 코드짜기위해 sqlalchemy잠시만 쓰는거
question_voter=db.Table(
    # primary 속성이 두개있으니까 many to many 관계 성립
    'question_voter',
    # 1이지워지면 이걸 포함하는 건 다 지워진다고봐야함
    # 하지만 프라이머리키 두개가 모두같은건 못씀
    #( user_id=1 question =1 )이 같은건 또 못쓴다는뜻
    db.Column('user_id',db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),primary_key=True),
    db.Column('question_id',db.Integer,db.ForeignKey('question.id',ondelete='CASCADE'),primary_key=True)
)
class Question(db.Model):
    # 다임 class=다 클다 
    id=db.Column(db.Integer,primary_key=True)
    subject=db.Column(db.String(200),nullable=False)
    content=db.Column(db.Text(),nullable=False)
    create_date=db.Column(db.DateTime(),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    user=db.relationship('User',backref=db.backref('question_set'))
    modify_date=db.Column(db.DateTime(),nullable=True)
    voter=db.relationship('User',secondary=question_voter,backref=db.backref('question_voter_set'))
    
    
answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)
class Answer(db.Model):
    # 다
    # 1이 지워지면 다도 다같이지 워져버림
    id=db.Column(db.Integer,primary_key=True)
    question_id=db.Column(db.Integer,db.ForeignKey('question.id',ondelete='CASCADE'))
    question=db.relationship('Question',backref=db.backref('answer_set'))
    content=db.Column(db.Text(),nullable=False)
    create_date=db.Column(db.DateTime(),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    user=db.relationship('User',backref=db.backref('answer_set'))
    modify_date=db.Column(db.DateTime(),nullable=True)
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))


class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(150),unique=True,nullable=False)
    password=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(200),nullable=False,unique=True)    

# snipet ${1|} 은 여러 메서드중하나 {$0} = 커서이동
