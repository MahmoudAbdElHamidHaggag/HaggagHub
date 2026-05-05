from sqlalchemy import String, DateTime, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from core.models.base.abstract_base import AbstractBaseModel


class License(AbstractBaseModel):
    __tablename__ = "licenses"

    tenant_id: Mapped[str] = mapped_column(String(36), nullable=False)
    hardware_id: Mapped[str] = mapped_column(String(200), nullable=False)
    license_key: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    encrypted_data: Mapped[str] = mapped_column(Text, nullable=False)  # Encrypted license data
    is_active: Mapped[bool] = mapped_column(default=True)
    issued_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    last_verified: Mapped[datetime] = mapped_column(nullable=True)
    verification_count: Mapped[int] = mapped_column(default=0)
    is_online_license: Mapped[bool] = mapped_column(default=False)
    subscription_plan_id: Mapped[str] = mapped_column(String(36), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
