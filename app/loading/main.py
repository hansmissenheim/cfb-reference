from typing import BinaryIO

from sqlmodel import Session


def load_save_file(save_file: BinaryIO, session: Session) -> None: ...
