from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from database.base import AbstractBaseModel


class Company(AbstractBaseModel):
    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(String(100))
    code: Mapped[str] = mapped_column(String(20), unique=True, index=True)