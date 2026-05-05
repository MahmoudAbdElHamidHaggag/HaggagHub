from sqlalchemy import String, ForeignKey, Boolean, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from core.models.base.abstract_base import AbstractBaseModel


class AccountType:
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"


class ChartOfAccounts(AbstractBaseModel):
    __tablename__ = "chart_of_accounts"

    tenant_id: Mapped[str] = mapped_column(String(36), ForeignKey('tenants.id'), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    account_type: Mapped[str] = mapped_column(String(20), nullable=False)
    parent_id: Mapped[str] = mapped_column(String(36), ForeignKey('chart_of_accounts.id'), nullable=True)
    level: Mapped[int] = mapped_column(default=1)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_leaf: Mapped[bool] = mapped_column(default=True)
    balance_type: Mapped[str] = mapped_column(String(10), default="debit")  # debit or credit
    tax_rate: Mapped[float] = mapped_column(default=0.0)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
