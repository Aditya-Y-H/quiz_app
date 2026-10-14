from helpers import verify_title
from quiz_app.models import Deck


def test_index(client, db):
    response = client.get("/")
    assert response.status_code == 200
    verify_title(response, "Quizzer")


def test_index_displays_decks_from_database(client, db):
    db.session.add(Deck(name="Network Basics", description="Networking fundamentals."))
    db.session.commit()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Network Basics" in response.data
    assert b"Networking fundamentals." in response.data
    assert b"0 questions" in response.data
    assert b"Sample Deck" not in response.data


def test_unknown_route_returns_404(client):
    assert client.get("/nope").status_code == 404
