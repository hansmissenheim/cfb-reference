from sqlmodel import Field, SQLModel


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


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    year: int
