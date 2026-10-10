from quiz_app.models import Deck, Question, User


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
            Deck(name="Geography", description="World geography", user=user),
            Deck(name="History", description="World history", user=user),
        ]
    )

    db.session.add(user)
    db.session.commit()
    db.session.expire_all()

    saved_user = db.session.get(User, user.id)
    assert saved_user is not None
    assert len(saved_user.decks) == 2
    assert all(deck.user_id == saved_user.id for deck in saved_user.decks)
