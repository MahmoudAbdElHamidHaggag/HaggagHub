from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings


local_engine = create_engine(settings.LOCAL_DB_URL, connect_args={"check_same_thread": False})


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=local_engine)


from sqlalchemy.orm import declarative_base
Base = declarative_base()