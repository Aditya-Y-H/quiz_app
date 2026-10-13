from flask import Blueprint, render_template

bp = Blueprint("main", __name__)


@bp.route("/")
@bp.route("/index")
@bp.route("/home")
def index():
    return render_template("index.html")
