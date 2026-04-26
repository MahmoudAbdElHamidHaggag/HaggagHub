from sqlalchemy import create_engine
from config import settings



ENGINES = {}


def get_engine(database_url: str):
    """
    Return cached engine or create new one
    """

    if database_url in ENGINES:
        return ENGINES[database_url]

    engine = create_engine(
        database_url,
        pool_pre_ping=True,
        pool_recycle=3600,
    )

    ENGINES[database_url] = engine
    return engine