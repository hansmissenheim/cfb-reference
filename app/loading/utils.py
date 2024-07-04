from sqlmodel import Session


class BaseLoader:
    def __init__(self, save_data, session: Session):
        self.save_data = save_data
        self.session = session

    def load(self):
        raise NotImplementedError
