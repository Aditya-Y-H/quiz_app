from helpers import verify_title


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    verify_title(response, "Quizzer")


def test_unknown_route_returns_404(client):
    assert client.get("/nope").status_code == 404
