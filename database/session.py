from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings


# =========================
# ENGINES
# =========================

# 🟢 LOCAL (SQLite)
local_engine = create_engine(
    settings.LOCAL_DB_URL,
    connect_args={"check_same_thread": False}
)

# 🔴 CENTRAL (PostgreSQL)
remote_engine = create_engine(
    settings.TENANT_DB_URL_TEMPLATE
)


# =========================
# SESSIONS
# =========================

LocalSession = sessionmaker(
    bind=local_engine,
    autoflush=False,
    autocommit=False
)

RemoteSession = sessionmaker(
    bind=remote_engine,
    autoflush=False,
    autocommit=False
)


# =========================
# GETTERS (IMPORTANT)
# =========================

def get_local_engine():
    return local_engine


def get_remote_engine():
    return remote_engine


def get_local_db():
    return LocalSession()


def get_remote_db():
    return RemoteSession()