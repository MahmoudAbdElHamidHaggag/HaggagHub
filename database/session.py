from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings


local_engine = create_engine(settings.LOCAL_DB_URL, connect_args={"check_same_thread": False})
LocalSessionLocal = sessionmaker(bind=local_engine)


remote_engine = create_engine(settings.REMOTE_DB_URL)
RemoteSessionLocal = sessionmaker(bind=remote_engine)

Base = declarative_base()