from sqlalchemy import String, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from core.models.base.abstract_base import AbstractBaseModel


class Tenant(AbstractBaseModel):
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    domain: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    subscription_plan_id: Mapped[str] = mapped_column(String(36), nullable=True)
    subscription_expiry: Mapped[datetime] = mapped_column(nullable=True)
    is_online_mode: Mapped[bool] = mapped_column(default=True)
    license_key: Mapped[str] = mapped_column(String(500), nullable=True)
    hardware_id: Mapped[str] = mapped_column(String(200), nullable=True)
    contact_email: Mapped[str] = mapped_column(String(100), nullable=True)
    contact_phone: Mapped[str] = mapped_column(String(50), nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    currency_code: Mapped[str] = mapped_column(String(3), default="EGP")
    settings: Mapped[str] = mapped_column(Text, nullable=True)  # JSON settings
