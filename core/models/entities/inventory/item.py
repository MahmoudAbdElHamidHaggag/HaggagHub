from sqlalchemy import String, Text, Numeric, ForeignKey, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column
from core.models.base.abstract_base import AbstractBaseModel


class Item(AbstractBaseModel):
    __tablename__ = "items"

    tenant_id: Mapped[str] = mapped_column(String(36), ForeignKey('tenants.id'), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    category_id: Mapped[str] = mapped_column(String(36), nullable=True)
    unit_id: Mapped[str] = mapped_column(String(36), nullable=True)
    cost_price: Mapped[float] = mapped_column(Numeric(15, 4), default=0.0000)
    selling_price: Mapped[float] = mapped_column(Numeric(15, 4), default=0.0000)
    min_stock: Mapped[float] = mapped_column(Numeric(15, 4), default=0.0000)
    max_stock: Mapped[float] = mapped_column(Numeric(15, 4), default=0.0000)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_service: Mapped[bool] = mapped_column(default=False)
    barcode: Mapped[str] = mapped_column(String(100), nullable=True)
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    tax_rate: Mapped[float] = mapped_column(Numeric(5, 4), default=0.0000)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
