import requests
from database.session import get_local_db, get_remote_db


class BaseManager:

    def __init__(self, model):
        self.model = model

    def is_online(self):
        try:
            requests.get("https://www.google.com", timeout=2)
            return True
        except:
            return False

    def save(self, data):
        if self.is_online():
            db = get_remote_db()
        else:
            db = get_local_db()

        obj = self.model(**data)
        db.add(obj)
        db.commit()
        db.close()

    def sync(self):
        if not self.is_online():
            return

        local_db = get_local_db()
        remote_db = get_remote_db()

        records = local_db.query(self.model).all()

        for record in records:
            remote_db.add(self.model(**record.__dict__))

        remote_db.commit()

        local_db.close()
        remote_db.close()