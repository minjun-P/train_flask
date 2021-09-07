from flask import Flask, make_response, jsonify, render_template, redirect
from flask.helpers import url_for
from flask.templating import render_template_string
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

login_manager = LoginManager()


# 로그인 매니저 설정


@login_manager.user_loader
def user_loader(user_id):
    # 로그인한 경우, user_id만을 넘긴다. 이 user_id를 기준으로 user객체를 리턴해서 유지시켜주는게 이 함수의 역할
    # 즉, user_id 기반으로 실제 user를 load해 오는 것.
    from .models import User

    # current_user에 집어넣을 것을 반환함.
    return User.query.filter_by(id=user_id).first()


@login_manager.unauthorized_handler
def unauthorized():
    from app.forms import LoginForm

    return redirect(url_for("detail.login_required"))


# ORM 내부 제약조건 명명 규칙을 정해주기! metadat변수에 넣어줄 것임.
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

from sqlalchemy import MetaData

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()


def page_not_found(e):
    return render_template("404.html"), 404


def server_error(e):
    return render_template("500.html"), 500


def create_app():
    app = Flask(__name__)

    # app 설정
    # app.config 는 사전 형식이지만 파이썬 파일에서 설정값을 불러올 수 있는 기능 제공
    app.config.from_envvar("APP_CONFIG_FILE")
    # ORM - DB 설정
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    # blueprint 넣기
    from .views import main_views
    from .views import detail_views

    app.register_blueprint(main_views.bp)
    app.register_blueprint(detail_views.bp)

    # 오류페이지 설정

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_error)

    # 로그인 매니저 설정
    login_manager.init_app(app)
    login_manager.session_protection = "strong"

    # 진자템플릿 필터 설정
    from app.filter import datetime_form

    app.jinja_env.filters["datetime"] = datetime_form

    return app
