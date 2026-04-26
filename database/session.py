from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

# SQLite (local)
local_engine = create_engine(settings.LOCAL_DB_URL)
LocalSession = sessionmaker(bind=local_engine)

# PostgreSQL (remote)
remote_engine = create_engine(settings.REMOTE_DB_URL)
RemoteSession = sessionmaker(bind=remote_engine)


def get_local_db():
    return LocalSession()


def get_remote_db():
    return RemoteSession()