from fastapi.testclient import TestClient
from sqlmodel import Session

from app.api.routes.games import get_game, get_teams_from_game
from app.models import Game


def test_get_game(db: Session):
    """Test retrieval of a real game and ensure a fake game returns None."""
    real_game = get_game("2025-01-27-washington", db)
    fake_game = get_game("2025-01-27-rutgers", db)
    assert isinstance(real_game, Game)
    assert real_game.home_score == 21
    assert real_game.away_score == 55
    assert fake_game is None


def test_get_teams_from_game(db: Session):
    """Test extraction of home and away teams from a game."""
    real_game = get_game("2025-01-27-washington", db)
    assert isinstance(real_game, Game)
    real_home, real_away = get_teams_from_game(real_game)
    assert real_home is not None
    assert real_away is not None
    assert real_home.school.name == "Washington"
    assert real_away.school.name == "Florida"


def test_game_page(client: TestClient):
    """Test the game page response for both existing and non-existing games."""
    response = client.get("/games/2025-01-27-washington")
    assert response.status_code == 200
    assert "Florida at Washington, January 27, 2025" in response.text

    response = client.get("/games/2025-01-27-rutgers")
    assert response.status_code == 404
    assert "Game not found" in response.text
