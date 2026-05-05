from sqlalchemy import String, Boolean, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from core.models.base.abstract_base import AbstractBaseModel


class Currency(AbstractBaseModel):
    __tablename__ = "currencies"

    code: Mapped[str] = mapped_column(String(3), unique=True, nullable=False)  # USD, EUR, EGP
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    symbol: Mapped[str] = mapped_column(String(5), nullable=False)
    exchange_rate: Mapped[float] = mapped_column(Numeric(10, 6), default=1.000000)
    is_base_currency: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    decimal_places: Mapped[int] = mapped_column(default=2)
