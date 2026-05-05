from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from core.models.base.abstract_base import AbstractBaseModel


class Company(AbstractBaseModel):
    __tablename__ = "companies"

    tenant_id: Mapped[str] = mapped_column(String(36), ForeignKey('tenants.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    commercial_name: Mapped[str] = mapped_column(String(200), nullable=True)
    tax_number: Mapped[str] = mapped_column(String(50), nullable=True)
    commercial_register: Mapped[str] = mapped_column(String(50), nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(100), nullable=True)
    website: Mapped[str] = mapped_column(String(200), nullable=True)
    logo_url: Mapped[str] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)