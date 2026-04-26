from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from database.base import AbstractBaseModel


class User(AbstractBaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(255))