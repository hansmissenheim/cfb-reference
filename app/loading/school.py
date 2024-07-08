from sqlmodel import Session, select

from app.loading.utils import BaseLoader, generate_url_slug
from app.models import School, SchoolStats


class SchoolLoader(BaseLoader):
    def __init__(self, save_data, year: int, session: Session):
        super().__init__(save_data, year, session)
        self.schools = all_schools_dict(session)

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

    def update_or_create_school(self, school_in):
        if school := self.schools.get(school_in.id):
            update_dict = school_in.model_dump(exclude={"id"})
            school.sqlmodel_update(update_dict)
        else:
            school = school_in
        return school


def all_schools_dict(session: Session):
    schools = session.exec(select(School)).all()
    return {school.id: school for school in schools}
