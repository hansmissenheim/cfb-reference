import re

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.api.routes.players import (
    get_player,
    get_players_alphabet,
    get_players_by_letter,
    get_random_players_by_letter,
)
from app.models import Player


def test_get_player(db: Session):
    """Test retrieval of a real player and ensure a fake player returns None."""
    real_player = get_player("arch-manning-1", db)
    fake_player = get_player("spongebob-squarepants-2", db)
    assert isinstance(real_player, Player)
    assert real_player.first_name == "Arch"
    assert real_player.last_name == "Manning"
    assert fake_player is None


def test_get_players_by_letter(db: Session):
    """Test retrieval of players by letter."""
    players = get_players_by_letter("A", db)
    assert len(players) == 300
    for player in players:
        assert player.last_name.startswith("A")


def test_get_random_players_by_letter(db: Session):
    """Test retrieval of random players by letter."""
    limit = 5
    players = get_random_players_by_letter("Z", db, limit=limit)
    assert len(players) <= limit
    for player in players:
        assert player.last_name.startswith("Z")


def test_get_players_alphabet(db: Session):
    """Test retrieval of players grouped by letter."""
    limit = 5
    players_dict = get_players_alphabet(db, limit=5)
    assert len(players_dict) == 26
    for letter, players in players_dict.items():
        assert len(players) <= limit
        assert players[0].last_name.startswith(letter)
        assert players[-1].last_name.startswith(letter)


def test_player_page(client: TestClient):
    """Test the player page response for both existing and non-existing players."""
    response = client.get("/players/arch-manning-1")
    assert response.status_code == 200
    assert "Arch Manning" in response.text

    response = client.get("/players/spongebob-squarepants-2")
    assert response.status_code == 404
    assert "Player not found" in response.text


def test_all_players_page(client: TestClient):
    """Test the all players page response."""
    response = client.get("/players")
    assert response.status_code == 200
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        assert f'<h1 class="text-4xl font-bold pb-2">{letter}</h1>' in response.text


def test_all_players_with_letter_page(client: TestClient):
    """Test the players by letter page response."""
    response = client.get("/players/letter/A")
    assert response.status_code == 200
    player_matches = re.findall(
        r'<span class="text-xl font-bold">(.+)</span>', response.text
    )
    assert len(player_matches) == 300
    for player_match in player_matches:
        assert player_match.startswith("A")
