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
