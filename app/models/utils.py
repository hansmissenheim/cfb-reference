from sqlmodel import Field, SQLModel


class Media(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(alias="MHTX")
    subtitle: str = Field(alias="MCTX")
    week: int = Field(alias="SEWN")
    year: int

    game_ea_id: int = Field(alias="SGNM", foreign_key="game.ea_id")
    school_id: int = Field(alias="TGID", foreign_key="school.id")
