from sqlmodel import Session, select

from app.loading.utils import BaseLoader
from app.models import Stadium


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


def all_stadiums_dict(session: Session):
    stadiums = session.exec(select(Stadium)).all()
    return {stadium.id: stadium for stadium in stadiums}
