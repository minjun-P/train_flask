from sqlalchemy.sql.schema import ForeignKey
from app import db

from flask_login import UserMixin

# 로그인 관련 설정


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pw = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    _class = db.Column(db.String(50), nullable=True)

    # 플라스크로그인 관련 유저 모델 필수요소 설정
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymus(self):
        return False

    def get_id(self):
        return str(self.id)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 외래키 설정
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    # 다른 모델이 해당 본 모델을 참조 가능하게 관계 객체 설정
    # User객체.question_set으로 본 모델 참조 가능
    user = db.relationship("User", backref=db.backref("question_set"))
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(
        db.Integer,
        db.ForeignKey("question.id", ondelete="CASCADE"),
        nullable=False,
    )
    question = db.relationship("Question", backref=db.backref("answer_set"))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)


class Question_A(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(), nullable=False)
    question_a_id = db.Column(
        db.Integer, db.ForeignKey("question_A.id"), nullable=False
    )
    question_a = db.relationship(
        "Question_A", backref=db.backref("comment_set")
    )
    create_date = db.Column(db.DateTime(), nullable=False)


class Faq(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
