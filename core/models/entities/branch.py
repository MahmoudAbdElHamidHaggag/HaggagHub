from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database.base import AbstractBaseModel


class Branch(AbstractBaseModel):
    __tablename__ = "branches"

    name: Mapped[str] = mapped_column(String(100))
    code: Mapped[str] = mapped_column(String(20), unique=True, index=True)

    company_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("companies.id"),
        index=True
    )