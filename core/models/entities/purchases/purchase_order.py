from sqlalchemy import String, Text, ForeignKey, Numeric, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from enum import Enum as PyEnum
from core.models.base.abstract_base import AbstractBaseModel


class PurchaseOrderStatus(PyEnum):
    DRAFT = "draft"
    SENT = "sent"
    APPROVED = "approved"
    RECEIVED = "received"
    CANCELLED = "cancelled"


class PurchaseOrder(AbstractBaseModel):
    __tablename__ = "purchase_orders"

    tenant_id: Mapped[str] = mapped_column(String(36), ForeignKey('tenants.id'), nullable=False)
    branch_id: Mapped[str] = mapped_column(String(36), ForeignKey('branches.id'), nullable=False)
    supplier_id: Mapped[str] = mapped_column(String(36), nullable=True)
    order_number: Mapped[str] = mapped_column(String(50), nullable=False)
    order_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    expected_delivery_date: Mapped[datetime] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(String(20), default=PurchaseOrderStatus.DRAFT.value)
    subtotal: Mapped[float] = mapped_column(Numeric(15, 4), default=0.0000)
    tax_amount: Mapped[float] = mapped_column(Numeric(15, 4), default=0.0000)
    discount_amount: Mapped[float] = mapped_column(Numeric(15, 4), default=0.0000)
    total_amount: Mapped[float] = mapped_column(Numeric(15, 4), default=0.0000)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    supplier_notes: Mapped[str] = mapped_column(Text, nullable=True)
    created_by: Mapped[str] = mapped_column(String(36), nullable=True)
    approved_by: Mapped[str] = mapped_column(String(36), nullable=True)
    approved_at: Mapped[datetime] = mapped_column(nullable=True)
