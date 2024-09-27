from pybo.models import Question,Answer

Question.query.count()
Answer.query.count()
Question.query.join(Answer).count()

Question.query.outerjoin(Answer).count()
# 질문개수+답변개수 더많아짐
Question.query.outerjoin(Answer).distinct().count()
Question.query.outerjoin(Answer).filter(
    Question.content.ilike('%파이썬%')|
    Answer.content.ilike('%파이썬%')
).distinct().count()