from sqlalchemy import String, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from core.models.base.abstract_base import AbstractBaseModel


class PurchaseOrderItem(AbstractBaseModel):
    __tablename__ = "purchase_order_items"

    purchase_order_id: Mapped[str] = mapped_column(String(36), ForeignKey('purchase_orders.id'), nullable=False)
    item_id: Mapped[str] = mapped_column(String(36), ForeignKey('items.id'), nullable=False)
    quantity: Mapped[float] = mapped_column(Numeric(15, 4), nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(15, 4), nullable=False)
    discount_percentage: Mapped[float] = mapped_column(Numeric(5, 4), default=0.0000)
    tax_rate: Mapped[float] = mapped_column(Numeric(5, 4), default=0.0000)
    total_amount: Mapped[float] = mapped_column(Numeric(15, 4), nullable=False)
    received_quantity: Mapped[float] = mapped_column(Numeric(15, 4), default=0.0000)
    notes: Mapped[str] = mapped_column(String(500), nullable=True)
