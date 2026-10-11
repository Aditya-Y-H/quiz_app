from pathlib import Path
import click

from flask import json
from flask.cli import with_appcontext

from quiz_app.models import Deck, Question
from extensions import db

SEED_FILE = Path("seed") / "decks.json"


@click.command("seed")
@with_appcontext
def seed():
    with SEED_FILE.open() as f:
        data = json.load(f)

    for datum in data:
        deck = db.session.scalar(db.select(Deck).where(Deck.slug == datum["slug"]))
        if deck is None:
            deck = Deck(slug=datum["slug"], user_id=None)
            db.session.add(deck)
        deck.name = datum["name"]
        deck.description = datum.get("description")

        deck.questions.clear()
        for question in datum["questions"]:
            a, b, c, d = question["options"]
            deck.questions.append(
                Question(
                    question=question["question"],
                    option_a=a,
                    option_b=b,
                    option_c=c,
                    option_d=d,
                    answer=question["answer"],
                )
            )
    db.session.commit()
