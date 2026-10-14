from flask import Blueprint, render_template, redirect, url_for

from extensions import db
from quiz_app.models import Deck
from quiz_app.forms import LoginForm, CreateUserForm

from collections.abc import Sequence

bp = Blueprint("main", __name__)


@bp.route("/")
@bp.route("/index")
@bp.route("/home")
def index():
    decks: Sequence[Deck] = db.session.scalars(db.select(Deck)).all()
    return render_template("index.html", decks=decks)


@bp.route("/login")
def login():
    form = LoginForm()

    if form.validate_on_submit():
        return redirect(url_for("index"))
    return render_template("login.html", form=form)


@bp.route("/register")
def register():
    form = CreateUserForm()

    if form.validate_on_submit():
        return redirect(url_for("index"))
    return render_template("register.html", form=form)
