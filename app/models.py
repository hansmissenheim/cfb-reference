from sqlmodel import Field, Relationship, SQLModel


class Player(SQLModel, table=True):
    id: int = Field(primary_key=True)
    first_name: str
    last_name: str
    position: int
    year: int


class School(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    nickname: str

    teams: list["Team"] = Relationship(back_populates="school")


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    year: int

    school_id: int | None = Field(default=None, foreign_key="school.id")
    school: School | None = Relationship(back_populates="teams")
