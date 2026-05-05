from sqlalchemy import String, Text, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from core.models.base.abstract_base import AbstractBaseModel


class JournalEntry(AbstractBaseModel):
    __tablename__ = "journal_entries"

    tenant_id: Mapped[str] = mapped_column(String(36), ForeignKey('tenants.id'), nullable=False)
    branch_id: Mapped[str] = mapped_column(String(36), ForeignKey('branches.id'), nullable=False)
    entry_number: Mapped[str] = mapped_column(String(50), nullable=False)
    entry_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    reference_type: Mapped[str] = mapped_column(String(50), nullable=True)  # purchase, sale, payment, etc.
    reference_id: Mapped[str] = mapped_column(String(36), nullable=True)
    total_debit: Mapped[float] = mapped_column(Numeric(15, 4), default=0.0000)
    total_credit: Mapped[float] = mapped_column(Numeric(15, 4), default=0.0000)
    is_posted: Mapped[bool] = mapped_column(default=False)
    posted_at: Mapped[datetime] = mapped_column(nullable=True)
    posted_by: Mapped[str] = mapped_column(String(36), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    created_by: Mapped[str] = mapped_column(String(36), nullable=True)
