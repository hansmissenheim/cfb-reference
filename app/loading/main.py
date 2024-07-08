from typing import Any, BinaryIO, Hashable

import ncaadb
import pandas as pd
from sqlmodel import Session

from app.loading.game import GameLoader
from app.loading.misc import CoachLoader, MediaLoader, StadiumLoader
from app.loading.player import PlayerLoader, PlayerStatsLoader
from app.loading.school import SchoolLoader

BASE_YEAR = 2013
TABLES = [
    "COCH",
    "MCOV",
    "PLAY",
    "PSDE",
    "PSOF",
    "PSOL",
    "PSKI",
    "PSKP",
    "SCHD",
    "SEAI",
    "STAD",
    "TEAM",
    "TSSE",
]
LOADERS = [
    StadiumLoader,
    SchoolLoader,
    PlayerLoader,
    PlayerStatsLoader,
    CoachLoader,
    GameLoader,
    MediaLoader,
]


class LoaderManager:
    def __init__(self, save_file: BinaryIO, session: Session):
        self.session = session
        self.save_data = self._parse_save_file(save_file)
        self.year = self.save_data["SEAI"][0]["SSYE"] + BASE_YEAR

    def _parse_save_file(
        self, save_file: BinaryIO
    ) -> dict[str, list[dict[Hashable, Any]]]:
        db_file = ncaadb.read_db(save_file)
        data = {
            table: db_file[table].reset_index().to_dict(orient="records")
            for table in TABLES
        }
        data["TEAM"] = (
            pd.merge(db_file["TEAM"], db_file["TSSE"], on="TGID", how="left")
            .convert_dtypes()
            .to_dict(orient="records")
        )
        return data

    def load_all(self):
        for loader_class in LOADERS:
            loader = loader_class(self.save_data, self.year, self.session)
            loader.load()


def load_save_file(save_file: BinaryIO, session: Session) -> None:
    loader = LoaderManager(save_file, session)
    loader.load_all()
