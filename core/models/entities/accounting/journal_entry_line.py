from sqlalchemy import String, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column
from core.models.base.abstract_base import AbstractBaseModel


class JournalEntryLine(AbstractBaseModel):
    __tablename__ = "journal_entry_lines"

    journal_entry_id: Mapped[str] = mapped_column(String(36), ForeignKey('journal_entries.id'), nullable=False)
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey('chart_of_accounts.id'), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    debit_amount: Mapped[float] = mapped_column(Numeric(15, 4), default=0.0000)
    credit_amount: Mapped[float] = mapped_column(Numeric(15, 4), default=0.0000)
    cost_center_id: Mapped[str] = mapped_column(String(36), nullable=True)
    project_id: Mapped[str] = mapped_column(String(36), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
