from flask import (
    Blueprint,
    url_for,
    render_template,
    request,
    redirect,
    flash,
    session,
)
from flask_login import login_user, current_user, logout_user, login_required

from app.models import User, Question, Question_A, Faq
from app.forms import LoginForm

bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("/")
def to_main():
    return redirect(url_for("main.main"))


@bp.route("/main", methods=["GET", "POST"])
def main():
    form = LoginForm()
    faq_list = Faq.query.limit(4).all()
    question_list = (
        Question.query.order_by(Question.create_date.desc()).limit(4).all()
    )
    question_a_list = (
        Question_A.query.order_by(Question_A.create_date.desc()).limit(4).all()
    )
    if form.validate_on_submit():
        id = form.id.data
        pw = form.pw.data
        user = User.query.filter_by(id=id).first()
        if user.pw == pw:
            login_user(user)
            flash("로그인 성공!")
            return redirect(url_for("main.main"))
        else:
            flash("계정 정보가 일치하지 않습니다")
            return redirect(url_for("main.main"))
    return render_template(
        "main.html",
        form=form,
        question_list=question_list,
        question_a_list=question_a_list,
        faq_list=faq_list,
    )


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.main"))


@bp.route("/test")
def test():
    return str(request.environ)
