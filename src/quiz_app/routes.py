from flask import Blueprint, render_template

from extensions import db
from quiz_app.models import Deck

from collections.abc import Sequence

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    decks: Sequence[Deck] = db.session.scalars(db.select(Deck)).all()
    return render_template("index.html", decks=decks)
