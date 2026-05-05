from sqlalchemy import String, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from core.models.base.abstract_base import AbstractBaseModel


class Branch(AbstractBaseModel):
    __tablename__ = "branches"

    tenant_id: Mapped[str] = mapped_column(String(36), ForeignKey('tenants.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(100), nullable=True)
    is_main_branch: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    manager_name: Mapped[str] = mapped_column(String(100), nullable=True)
    manager_phone: Mapped[str] = mapped_column(String(50), nullable=True)
    warehouse_id: Mapped[str] = mapped_column(String(36), nullable=True)  # Default warehouse
    financial_dimension_id: Mapped[str] = mapped_column(String(36), nullable=True)