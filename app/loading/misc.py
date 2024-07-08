from sqlmodel import Session, select

from app.loading.school import all_teams_dict
from app.loading.utils import BaseLoader
from app.models import Coach, Media, Stadium


class StadiumLoader(BaseLoader):
    def __init__(self, save_data, year: int, session: Session):
        super().__init__(save_data, year, session)
        self.stadiums = all_stadiums_dict(session)

    def load(self):
        for row in self.save_data["STAD"]:
            self.process_stadium(row)
        self.session.commit()

    def process_stadium(self, row):
        stadium_in = Stadium(**row)
        stadium = self.update_or_create_stadium(stadium_in)
        self.session.add(stadium)

    def update_or_create_stadium(self, stadium_in):
        if stadium := self.stadiums.get(stadium_in.id):
            update_dict = stadium_in.model_dump()
            stadium.sqlmodel_update(update_dict)
        else:
            stadium = stadium_in
        return stadium


class CoachLoader(BaseLoader):
    def __init__(self, save_data, year: int, session: Session):
        super().__init__(save_data, year, session)
        self.coaches = all_coaches_dict(session)
        self.teams = all_teams_dict(session)

    def load(self):
        for row in self.save_data["COCH"]:
            self.process_coach(row)
        self.session.commit()

    def process_coach(self, row):
        coach_in = Coach(**row)
        coach = self.update_or_create_coach(coach_in)
        self.add_team_to_coach(coach, row["TGID"])
        self.session.add(coach)

    def update_or_create_coach(self, coach_in):
        if coach := self.coaches.get(coach_in.id):
            update_dict = coach_in.model_dump()
            coach.sqlmodel_update(update_dict)
        else:
            coach = coach_in
        return coach

    def add_team_to_coach(self, coach, school_id):
        team = self.teams.get((school_id, self.year))
        if team and team not in coach.teams:
            if team not in coach.teams:
                coach.teams.append(team)


class MediaLoader(BaseLoader):
    def __init__(self, save_data, year: int, session: Session):
        super().__init__(save_data, year, session)
        self.media = all_media_dict(session)

    def load(self):
        for row in self.save_data["MCOV"]:
            self.process_media(row)
        self.session.commit()

    def process_media(self, row):
        media_in = Media(**row, year=self.year)
        media = self.update_or_create_media(media_in)
        self.session.add(media)

    def update_or_create_media(self, media_in):
        if media := self.media.get((media_in.game_ea_id, self.year)):
            update_dict = media_in.model_dump(exclude={"id"})
            media.sqlmodel_update(update_dict)
        else:
            media = media_in
        return media


def all_stadiums_dict(session: Session):
    stadiums = session.exec(select(Stadium)).all()
    return {stadium.id: stadium for stadium in stadiums}


def all_coaches_dict(session: Session):
    coaches = session.exec(select(Coach)).all()
    return {coach.id: coach for coach in coaches}


def all_media_dict(session: Session):
    medias = session.exec(select(Media)).all()
    return {(media.game_ea_id, media.year): media for media in medias}
