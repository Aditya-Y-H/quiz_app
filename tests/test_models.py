from quiz_app.models import Deck, Question, User

import pytest

from sqlalchemy.exc import IntegrityError
from sqlalchemy import text


def test_deck_has_many_questions(db):
    user = User(name="quizzer", hashed_password="hashed-value")
    deck = Deck(name="Geography", description="World geography", user=user)
    deck.questions.extend(
        [
            Question(
                question="Largest ocean?",
                option_a="Atlantic",
                option_b="Indian",
                option_c="Arctic",
                option_d="Pacific",
                answer="D",
            ),
            Question(
                question="Smallest continent?",
                option_a="Australia",
                option_b="Europe",
                option_c="Antarctica",
                option_d="South America",
                answer="A",
            ),
        ]
    )

    db.session.add(deck)
    db.session.commit()
    db.session.expire_all()

    saved_deck = db.session.get(Deck, deck.id)
    assert saved_deck is not None
    assert len(saved_deck.questions) == 2
    assert all(question.deck_id == saved_deck.id for question in saved_deck.questions)
    assert saved_deck.user.name == "quizzer"
    assert saved_deck.user_id == user.id


def test_user_has_many_decks(db):
    user = User(name="quizzer", hashed_password="hashed-value")
    user.decks.extend(
        [
            Deck(
                name="Geography",
                description="World geography",
                user=user,
                slug="geography",
            ),
            Deck(
                name="History", description="World history", user=user, slug="history"
            ),
        ]
    )

    db.session.add(user)
    db.session.commit()
    db.session.expire_all()

    saved_user = db.session.get(User, user.id)
    assert saved_user is not None
    assert len(saved_user.decks) == 2
    assert all(deck.user_id == saved_user.id for deck in saved_user.decks)


def test_deck_slug_is_unique(db):
    deck1 = Deck(name="Geography", description="World geography", slug="geography")
    deck2 = Deck(name="History", description="World history", slug="geography")

    db.session.add(deck1)
    db.session.commit()

    db.session.add(deck2)

    with pytest.raises(
        IntegrityError,
        match="UNIQUE constraint failed|duplicate key value violates unique constraint",
    ):
        db.session.commit()

    db.session.rollback()


def test_question_deck_cascade_delete(db):
    deck = Deck(name="Geography", description="World geography")
    question1 = Question(
        question="Largest ocean?",
        option_a="Atlantic",
        option_b="Indian",
        option_c="Arctic",
        option_d="Pacific",
        answer="D",
        deck=deck,
    )
    question2 = Question(
        question="Smallest continent?",
        option_a="Australia",
        option_b="Europe",
        option_c="Antarctica",
        option_d="South America",
        answer="A",
        deck=deck,
    )

    db.session.add(deck)
    db.session.commit()
    db.session.expire_all()

    saved_deck = db.session.get(Deck, deck.id)
    assert saved_deck is not None
    assert len(saved_deck.questions) == 2

    db.session.delete(saved_deck)
    db.session.commit()
    db.session.expire_all()

    deleted_deck = db.session.get(Deck, deck.id)
    assert deleted_deck is None

    deleted_question1 = db.session.get(Question, question1.id)
    deleted_question2 = db.session.get(Question, question2.id)
    assert deleted_question1 is None
    assert deleted_question2 is None


def test_sqlite_foreign_keys_are_enabled(db):
    assert db.engine.dialect.name == "sqlite"
    assert db.session.execute(text("PRAGMA foreign_keys")).scalar_one() == 1


def test_question_requires_existing_deck(db):
    question = Question(
        question="Largest ocean?",
        option_a="Atlantic",
        option_b="Indian",
        option_c="Arctic",
        option_d="Pacific",
        answer="D",
        deck_id=999,
    )
    db.session.add(question)

    with pytest.raises(IntegrityError):
        db.session.commit()

    db.session.rollback()


def test_question_answer_must_be_a_valid_option(db):
    deck = Deck(name="Geography")
    question = Question(
        question="Largest ocean?",
        option_a="Atlantic",
        option_b="Indian",
        option_c="Arctic",
        option_d="Pacific",
        answer="E",
        deck=deck,
    )
    db.session.add(question)

    with pytest.raises(IntegrityError):
        db.session.commit()

    db.session.rollback()


@pytest.mark.parametrize("missing_field", ["answer", "deck_id"])
def test_question_required_fields_cannot_be_null(db, missing_field):
    question_data = {
        "question": "Largest ocean?",
        "option_a": "Atlantic",
        "option_b": "Indian",
        "option_c": "Arctic",
        "option_d": "Pacific",
        "answer": "D",
        "deck_id": 1,
    }
    question_data[missing_field] = None
    db.session.add(Question(**question_data))

    with pytest.raises(IntegrityError):
        db.session.commit()

    db.session.rollback()


def test_deleting_user_deletes_decks_and_questions(db):
    user = User(name="quizzer", hashed_password="hashed-value")
    deck = Deck(name="Geography", user=user)
    question = Question(
        question="Largest ocean?",
        option_a="Atlantic",
        option_b="Indian",
        option_c="Arctic",
        option_d="Pacific",
        answer="D",
        deck=deck,
    )
    db.session.add(user)
    db.session.commit()
    user_id, deck_id, question_id = user.id, deck.id, question.id

    db.session.delete(user)
    db.session.commit()

    assert db.session.get(User, user_id) is None
    assert db.session.get(Deck, deck_id) is None
    assert db.session.get(Question, question_id) is None


def test_removing_question_from_deck_deletes_it(db):
    deck = Deck(name="Geography")
    removed_question = Question(
        question="Largest ocean?",
        option_a="Atlantic",
        option_b="Indian",
        option_c="Arctic",
        option_d="Pacific",
        answer="D",
        deck=deck,
    )
    retained_question = Question(
        question="Smallest continent?",
        option_a="Australia",
        option_b="Europe",
        option_c="Antarctica",
        option_d="South America",
        answer="A",
        deck=deck,
    )
    db.session.add(deck)
    db.session.commit()
    removed_question_id = removed_question.id
    retained_question_id = retained_question.id

    deck.questions.remove(removed_question)
    db.session.commit()

    assert db.session.get(Question, removed_question_id) is None
    assert db.session.get(Question, retained_question_id) is not None
