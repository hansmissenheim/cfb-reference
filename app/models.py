from sqlmodel import Field, SQLModel


class Player(SQLModel, table=True):
    id: int = Field(primary_key=True)
    first_name: str
    last_name: str
    position: int
    year: int


class PlayerUpdate(Player):
    first_name: str | None = None
    last_name: str | None = None
    position: int | None = None
    year: int | None = None
