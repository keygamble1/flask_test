from flask import Flask
from wtforms import EmailField, PasswordField, StringField,TextAreaField
from wtforms.validators import DataRequired,Length,EqualTo,Email
from flask_wtf import FlaskForm

# 인터프리터에서 다시 실행한후에 pip install행햐ㅏㅁ

class QuestionForm(FlaskForm):
    subject=StringField('제목',validators=[DataRequired('제목필수')])
    # datarequired 검증 폼은 검증을위한것 알아서 체크하도록 냅둠
    
    content=TextAreaField('내용',validators=[DataRequired('내용필수')])

class AnswerForm(FlaskForm):
    content=TextAreaField('질문내용',validators=[DataRequired('답변내용필수')])

class UserCreateForm(FlaskForm):
    username=StringField('사용자이름',validators=[DataRequired(),Length(min=3,max=25)])
    password1=PasswordField('비밀번호',validators=[DataRequired(),
                                EqualTo('password2','비밀번호일치x')])
    password2=PasswordField('비밀번호확인',validators=[DataRequired()])
    email=EmailField('이메일',validators=[DataRequired(),Email()])
class UserLoginForm(FlaskForm):
    username=StringField('사용자이름',validators=[DataRequired(),Length(min=3,max=25)])
    password=PasswordField('비밀번호',validators=[DataRequired()])
    # tuple 수정불가
     