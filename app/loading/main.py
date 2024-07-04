from typing import Any, BinaryIO, Hashable

import ncaadb
from sqlmodel import Session

from app.loading.misc import StadiumLoader

TABLES = ["STAD"]
LOADERS = [StadiumLoader]


class LoaderManager:
    def __init__(self, save_file: BinaryIO, session: Session):
        self.session = session
        self.save_data = self._parse_save_file(save_file)

    def _parse_save_file(
        self, save_file: BinaryIO
    ) -> dict[str, list[dict[Hashable, Any]]]:
        db_file = ncaadb.read_db(save_file)
        return {table: db_file[table].to_dict(orient="records") for table in TABLES}

    def load_all(self):
        for loader_class in LOADERS:
            loader = loader_class(self.save_data, self.session)
            loader.load()


def load_save_file(save_file: BinaryIO, session: Session) -> None:
    loader = LoaderManager(save_file, session)
    loader.load_all()
