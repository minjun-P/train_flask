from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    id = StringField("ID", validators=[DataRequired("id를 입력해주세요")])
    pw = PasswordField("비밀번호", validators=[DataRequired("pw를 입력해주세요")])
    login = SubmitField("로그인")


class QuestionForm(FlaskForm):
    subject = StringField("제목", validators=[DataRequired("제목은 필수입력 항목입니다.")])
    content = TextAreaField("내용", validators=[DataRequired("내용은 필수입력 항목입니다.")])


class FaqForm(FlaskForm):
    subject = StringField("제목", validators=[DataRequired("제목은 필수입력 항목입니다.")])
    content = TextAreaField("내용", validators=[DataRequired("내용은 필수입력 항목입니다.")])
