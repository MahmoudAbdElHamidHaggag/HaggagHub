from sqlalchemy import String, Text, ForeignKey, Numeric, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from enum import Enum as PyEnum
from core.models.base.abstract_base import AbstractBaseModel


class TransactionType(PyEnum):
    PURCHASE = "purchase"
    PURCHASE_RETURN = "purchase_return"
    SALE = "sale"
    SALE_RETURN = "sale_return"
    TRANSFER = "transfer"
    ADJUSTMENT = "adjustment"
    PRODUCTION = "production"
    CONSUMPTION = "consumption"


class ItemTransaction(AbstractBaseModel):
    __tablename__ = "item_transactions"

    tenant_id: Mapped[str] = mapped_column(String(36), ForeignKey('tenants.id'), nullable=False)
    item_id: Mapped[str] = mapped_column(String(36), ForeignKey('items.id'), nullable=False)
    warehouse_id: Mapped[str] = mapped_column(String(36), ForeignKey('warehouses.id'), nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(50), nullable=False)
    reference_type: Mapped[str] = mapped_column(String(50), nullable=True)  # purchase_order, sale_invoice, etc.
    reference_id: Mapped[str] = mapped_column(String(36), nullable=True)
    quantity: Mapped[float] = mapped_column(Numeric(15, 4), nullable=False)
    unit_cost: Mapped[float] = mapped_column(Numeric(15, 4), default=0.0000)
    total_cost: Mapped[float] = mapped_column(Numeric(15, 4), default=0.0000)
    transaction_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    created_by: Mapped[str] = mapped_column(String(36), nullable=True)
    branch_id: Mapped[str] = mapped_column(String(36), ForeignKey('branches.id'), nullable=True)
