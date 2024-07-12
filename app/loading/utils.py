import re

from sqlmodel import Session


class BaseLoader:
    def __init__(self, save_data, year: int, session: Session):
        self.save_data = save_data
        self.session = session
        self.year = year

    def load(self):
        raise NotImplementedError


def generate_url_slug(string: str) -> str:
    url_slug = string.replace(" ", "-").lower()
    return re.sub(r"[^a-z0-9-]", "", url_slug)
