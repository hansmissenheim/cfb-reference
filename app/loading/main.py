from typing import Any, BinaryIO, Hashable

import ncaadb
from sqlmodel import Session

from app.loading.misc import StadiumLoader
from app.loading.school import SchoolLoader

BASE_YEAR = 2013
TABLES = ["SEAI", "STAD", "TEAM"]
LOADERS = [StadiumLoader, SchoolLoader]


class LoaderManager:
    def __init__(self, save_file: BinaryIO, session: Session):
        self.session = session
        self.save_data = self._parse_save_file(save_file)
        self.year = self.save_data["SEAI"][0]["SSYE"] + BASE_YEAR

    def _parse_save_file(
        self, save_file: BinaryIO
    ) -> dict[str, list[dict[Hashable, Any]]]:
        db_file = ncaadb.read_db(save_file)
        return {table: db_file[table].to_dict(orient="records") for table in TABLES}

    def load_all(self):
        for loader_class in LOADERS:
            loader = loader_class(self.save_data, self.year, self.session)
            loader.load()


def load_save_file(save_file: BinaryIO, session: Session) -> None:
    loader = LoaderManager(save_file, session)
    loader.load_all()
