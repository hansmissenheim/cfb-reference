from typing import BinaryIO

import ncaadb
from sqlmodel import Session

LOADERS = []


class LoaderManager:
    def __init__(self, save_file: BinaryIO, session: Session):
        self.session = session
        self.save_data = ncaadb.read_db(save_file)

    def load_all(self):
        for loader_class in LOADERS:
            loader_class.load()


def load_save_file(save_file: BinaryIO, session: Session) -> None: ...
