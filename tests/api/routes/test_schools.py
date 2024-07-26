import re

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.api.routes.schools import get_all_schools, get_school, get_team
from app.models import School, Team


def test_get_school(db: Session):
    """Test retrieval of a real school and ensure a fake school returns None."""
    real_school = get_school("arizona-state", db)
    fake_school = get_school("nyu", db)
    assert isinstance(real_school, School)
    assert real_school.name == "Arizona State"
    assert fake_school is None


def test_get_all_schools(db: Session):
    """Test retrieval of all schools."""
    schools = get_all_schools(db)
    assert len(schools) == 131
    assert all(isinstance(school, School) for school in schools)


def test_get_team(db: Session):
    """Test retrieval of a real team and ensure a fake team returns None."""
    real_team = get_team(1, 2024, db)
    fake_team = get_team(999, 2024, db)
    assert isinstance(real_team, Team)
    assert real_team.school.name == "Air Force"
    assert real_team.year == 2024
    assert fake_team is None


def test_school_page(client: TestClient):
    """Test the school page response for both existing and non-existing schools."""
    response = client.get("/schools/arizona-state")
    assert response.status_code == 200
    assert "Arizona State Sun Devils School History" in response.text

    response = client.get("/schools/nyu")
    assert response.status_code == 404
    assert "School not found" in response.text


def test_all_schools_page(client: TestClient):
    """Test the all schools page response."""
    response = client.get("/schools")
    assert response.status_code == 200
    school_matches = re.findall(r'<a href="/schools/(.+)">', response.text)
    assert len(school_matches) == 131


def test_team_page(client: TestClient):
    """Test the team page response for both existing and non-existing teams."""
    response = client.get("/schools/arizona-state/2024")
    assert response.status_code == 200
    assert "2024 Arizona State Sun Devils Stats" in response.text

    response = client.get("/schools/nyu/2024")
    assert response.status_code == 404
    assert "School not found" in response.text

    response = client.get("/schools/arizona-state/2025")
    assert response.status_code == 404
    assert "Team not found" in response.text
