from flask import Blueprint, url_for, render_template, request, redirect, flash
from flask_login import login_user, current_user, logout_user, login_required

from app.forms import LoginForm, QuestionForm, FaqForm
from app.models import User, Question, Question_A, Answer, Comment, Faq
from app import db


from datetime import datetime

bp = Blueprint("detail", __name__, url_prefix="/detail")


@bp.route("/faq")
def faq_list():
    faq_list = Faq.query.order_by(Faq.id.desc()).all()
    return render_template("faq_list.html", faq_list=faq_list)


@bp.route("/question")
def question_list():
    page = request.args.get("page", type=int, default=1)
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page, per_page=10)
    return render_template(
        "question/question_list.html", question_list=question_list
    )


@bp.route("/question_detail/<int:question_id>", methods=["GET", "POST"])
def question_detail(question_id):
    question = Question.query.get(question_id)
    if request.method == "POST":
        db.session.delete(question)
        db.session.commit()
        return redirect(url_for("detail.question_list"))
    return render_template("question/question_detail.html", question=question)


@bp.route("/question_create", methods=["GET", "POST"])
@login_required
def question_create():
    form = QuestionForm()
    if request.method == "POST" and form.validate_on_submit():
        subject = form.subject.data
        content = form.content.data
        question = Question(
            subject=subject,
            content=content,
            create_date=datetime.now(),
            user_id=current_user.get_id(),
        )
        db.session.add(question)
        db.session.commit()
        return redirect(url_for("detail.question_list"))

    return render_template("question/question_create.html", form=form)


@bp.route("/login_required", methods=["GET", "POST"])
def login_required():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
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
    return render_template("login_required.html", form=form)


@bp.route("/anonymous_list")
def anonymous():
    page = request.args.get("page", type=int, default=1)
    question_list = Question_A.query.order_by(Question_A.create_date.desc())
    question_list = question_list.paginate(page, per_page=10)
    return render_template(
        "question/question_a_list.html", question_list=question_list
    )


@bp.route("/anonymous_detail/<int:question_id>", methods=["GET", "POST"])
def a_detail(question_id):
    question = Question_A.query.get(question_id)
    if request.method == "POST":
        db.session.delete(question)
        db.session.commit()
        return redirect(url_for("detail.anonymous"))
    return render_template("question/question_a_detail.html", question=question)


@bp.route("/question_a_create", methods=["GET", "POST"])
def question_a_create():
    form = QuestionForm()
    if request.method == "POST" and form.validate_on_submit():
        subject = form.subject.data
        content = form.content.data
        question = Question_A(
            subject=subject, content=content, create_date=datetime.now()
        )
        db.session.add(question)
        db.session.commit()
        return redirect(url_for("detail.anonymous"))

    return render_template("question/question_a_create.html", form=form)


@bp.route("/answer/<int:question_id>", methods=["POST"])
def answer(question_id):
    if request.method == "POST":
        print("gd")
        content = request.form["answer"]
        print(content)
        question_id = question_id
        answer = Answer(
            question_id=question_id, content=content, create_date=datetime.now()
        )
        db.session.add(answer)
        db.session.commit()
        return redirect(
            url_for("detail.question_detail", question_id=question_id)
        )
    else:
        return "잘못된 접근입니다."


@bp.route("/answer_delete/<int:answer_id>")
def answer_delete(answer_id):
    answer = Answer.query.get(answer_id)
    question_id = answer.question_id
    db.session.delete(answer)
    db.session.commit()
    return redirect(url_for("detail.question_detail", question_id=question_id))


@bp.route("comment/<int:question_id>", methods=["POST"])
def comment_create(question_id):
    if request.method == "POST":
        content = request.form["comment"]
        comment = Comment(
            question_a_id=question_id,
            content=content,
            create_date=datetime.now(),
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("detail.a_detail", question_id=question_id))


@bp.route("/comment_delete/<int:comment_id>")
def comment_delete(comment_id):
    comment = Comment.query.get(comment_id)
    question_id = comment.question_a_id
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("detail.a_detail", question_id=question_id))


@bp.route("/faq_create", methods=["GET", "POST"])
def faq_create():
    form = FaqForm()
    if request.method == "POST" and form.validate_on_submit():
        subject = form.subject.data
        content = form.content.data
        faq = Faq(subject=subject, content=content)
        db.session.add(faq)
        db.session.commit()
        return redirect(url_for("detail.faq_list"))
    return render_template("faq_create.html", form=form)
