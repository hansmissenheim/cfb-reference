from fastapi.testclient import TestClient
from sqlmodel import Session

from app.api.routes.utils import (
    get_coverage_leaders,
    get_media,
    get_pass_rushing_leaders,
    get_passing_leaders,
    get_players_from_search,
    get_random_players,
    get_receiving_leaders,
    get_rushing_leaders,
    get_schools_from_search,
    get_top_25_teams,
    get_trending_players,
    get_year,
)
from app.models import (
    Media,
    Player,
    PlayerSeasonDefenseStats,
    PlayerSeasonOffenseStats,
    School,
)


def test_get_year(db: Session):
    """Test the retrieval of the current year from the database."""
    year = get_year(db)
    assert year == 2024


def test_get_random_players(db: Session):
    """Test the retrieval of random players from the database."""
    players = get_random_players(db, limit=12)
    assert len(players) == 12
    assert all(isinstance(player, Player) for player in players)


def test_get_trending_players(db: Session):
    """Test the retrieval of trending players from the database."""
    players = get_trending_players(db, limit=5)
    assert len(players) == 5
    assert all(isinstance(player, Player) for player in players)

    overalls = [player.attributes.overall for player in players]
    assert sorted(overalls, reverse=True) == overalls


def test_get_passing_leaders(db: Session):
    """Test the retrieval of passing leaders from the database."""
    year = get_year(db)
    leaders = get_passing_leaders(year, db, limit=10)
    assert len(leaders) == 10
    assert all(isinstance(player, Player) for player, _ in leaders)
    assert all(isinstance(stats, PlayerSeasonOffenseStats) for _, stats in leaders)

    pass_yards = [stats.pass_yards for _, stats in leaders]
    assert sorted(pass_yards, reverse=True) == pass_yards


def test_get_rushing_leaders(db: Session):
    """Test the retrieval of rushing leaders from the database."""
    year = get_year(db)
    leaders = get_rushing_leaders(year, db, limit=10)
    assert len(leaders) == 10
    assert all(isinstance(player, Player) for player, _ in leaders)
    assert all(isinstance(stats, PlayerSeasonOffenseStats) for _, stats in leaders)

    rush_yards = [stats.rush_yards for _, stats in leaders]
    assert sorted(rush_yards, reverse=True) == rush_yards


def test_get_receiving_leaders(db: Session):
    """Test the retrieval of receiving leaders from the database."""
    year = get_year(db)
    leaders = get_receiving_leaders(year, db, limit=10)
    assert len(leaders) == 10
    assert all(isinstance(player, Player) for player, _ in leaders)
    assert all(isinstance(stats, PlayerSeasonOffenseStats) for _, stats in leaders)

    recieving_yards = [stats.recieving_yards for _, stats in leaders]
    assert sorted(recieving_yards, reverse=True) == recieving_yards


def test_get_pass_rushing_leaders(db: Session):
    """Test the retrieval of pass rushing leaders from the database."""
    year = get_year(db)
    leaders = get_pass_rushing_leaders(year, db, limit=10)
    assert len(leaders) == 10
    assert all(isinstance(player, Player) for player, _ in leaders)
    assert all(isinstance(stats, PlayerSeasonDefenseStats) for _, stats in leaders)

    full_sacks = [stats.full_sacks for _, stats in leaders]
    assert sorted(full_sacks, reverse=True) == full_sacks


def test_get_coverage_leaders(db: Session):
    """Test the retrieval of coverage leaders from the database."""
    year = get_year(db)
    leaders = get_coverage_leaders(year, db, limit=10)
    assert len(leaders) == 10
    assert all(isinstance(player, Player) for player, _ in leaders)
    assert all(isinstance(stats, PlayerSeasonDefenseStats) for _, stats in leaders)
    interceptions = [stats.interceptions for _, stats in leaders]
    assert sorted(interceptions, reverse=True) == interceptions


def test_get_top_25_teams(db: Session):
    """Test the retrieval of the top 25 teams from the database."""
    year = get_year(db)
    teams = get_top_25_teams(year, db)
    assert len(teams) == 25
    assert all(team.stats.bcs_rank in range(1, 26) for team in teams)

    ranks = [team.stats.bcs_rank for team in teams]
    assert sorted(ranks) == ranks


def test_get_media(db: Session):
    """Test the retrieval of media from the database."""
    year = get_year(db)
    media = get_media(year, db, limit=20)
    assert len(media) <= 20
    assert all(isinstance(medium, Media) for medium in media)

    school_ids = [medium.school_id for medium in media]
    assert len(set(school_ids)) == len(school_ids)


def test_get_players_from_search(db: Session):
    """Test the retrieval of players from the database."""
    players = get_players_from_search("Mann", db, limit=5)
    assert len(players) == 5
    assert all(isinstance(player, Player) for player in players)
    for player in players:
        assert player.first_name.lower().startswith(
            "mann"
        ) or player.last_name.lower().startswith("mann")


def test_get_schools_from_search(db: Session):
    """Test the retrieval of schools from the database."""
    schools = get_schools_from_search("Mich", db)
    assert len(schools) == 2
    assert all(isinstance(school, School) for school in schools)
    assert all(school.name.lower().startswith("mich") for school in schools)


def test_home_page(client: TestClient):
    """Test the home page response."""
    response = client.get("/")
    assert response.status_code == 200
    assert "College Football Players" in response.text
    assert "Trending Players" in response.text
    assert "Passing Leaders" in response.text
    assert "Rushing Leaders" in response.text
    assert "Receiving Leaders" in response.text
    assert "Pass Rushing Leaders" in response.text
    assert "Coverage Leaders" in response.text
    assert "2024 Top 25 Ranked" in response.text
    assert "College Football News" in response.text


def test_search_route(client: TestClient):
    """Test the search route response."""
    response = client.post("/search", data={"search": "Mich"})
    assert response.status_code == 200
    assert response.text.count('href="/players') == 10
    assert response.text.count('href="/schools') == 2

    response = client.post("/search", data={"search": "Xyz"})
    assert response.status_code == 200
    assert response.text.count('href="/players') == 0
    assert response.text.count('href="/schools') == 0


def test_upload_form_page(client: TestClient):
    """Test the upload form page response."""
    response = client.get("/upload")
    assert response.status_code == 200
    assert "Upload Save File" in response.text


def test_upload_file(client: TestClient):
    """Test the upload file response."""
    with open("tests/data/init.USR-DATA", "rb") as file:
        response = client.post("/upload", files={"save_file_upload": file})
    assert response.status_code == 200
    assert response.text == '{"status":"success"}'

    with open("tests/api/routes/test_utils.py", "rb") as file:
        response = client.post("/upload", files={"save_file_upload": file})
    assert response.status_code == 200
    assert response.text == "Invalid file format. Please upload a NCAA 14 DB file."
