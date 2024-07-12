from sqlmodel import Session, select

from app.loading.utils import BaseLoader, generate_url_slug
from app.models import School, SchoolStats, Team, TeamStats


class SchoolLoader(BaseLoader):
    def __init__(self, save_data, year: int, session: Session):
        super().__init__(save_data, year, session)
        self.schools = all_schools_dict(session)
        self.teams = all_teams_dict(session)

    def load(self):
        for row in self.save_data["TEAM"]:
            self.process_school(row)
        self.session.commit()

    def process_school(self, row):
        school_in = School(**row)
        school_in.stats = SchoolStats(**row)
        school_in.url_slug = generate_url_slug(school_in.name)

        school = self.update_or_create_school(school_in)
        self.session.add(school)

        team_stats_in = TeamStats(**row)
        team = self.update_or_create_team(school.id, team_stats_in)
        self.session.add(team)

    def update_or_create_school(self, school_in):
        if school := self.schools.get(school_in.id):
            update_dict = school_in.model_dump(exclude={"id"})
            school.sqlmodel_update(update_dict)
        else:
            school = school_in
        return school

    def update_or_create_team(self, school_id, team_stats_in):
        if team := self.teams.get((school_id, self.year)):
            update_dict = team_stats_in.model_dump(
                exclude={"team_id"}, exclude_none=True
            )
            team.stats.sqlmodel_update(update_dict)
        else:
            team = Team(school_id=school_id, year=self.year, stats=team_stats_in)
        return team


def all_schools_dict(session: Session):
    schools = session.exec(select(School)).all()
    return {school.id: school for school in schools}


def all_teams_dict(session: Session):
    teams = session.exec(select(Team)).all()
    return {(team.school_id, team.year): team for team in teams}
