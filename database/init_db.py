from database.base import Base
from database.session import get_local_engine, get_remote_engine
from sqlalchemy import text


def is_online():
    try:
        engine = get_remote_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def init_local():
    engine = get_local_engine()
    Base.metadata.create_all(bind=engine)
    print("🟢 LOCAL SQLite ready")


def init_remote():
    engine = get_remote_engine()
    Base.metadata.create_all(bind=engine)
    print("🟣 CENTRAL PostgreSQL ready")


def main():
    if is_online():
        print("ONLINE DETECTED → CENTRAL")
        init_remote()
    else:
        print("OFFLINE DETECTED → LOCAL")
        init_local()


if __name__ == "__main__":
    main()