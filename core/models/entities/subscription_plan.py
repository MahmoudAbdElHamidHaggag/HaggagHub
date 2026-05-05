from sqlalchemy import String, Boolean, Text, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from core.models.base.abstract_base import AbstractBaseModel


class SubscriptionPlan(AbstractBaseModel):
    __tablename__ = "subscription_plans"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    monthly_price: Mapped[float] = mapped_column(Numeric(10, 2), default=0.00)
    yearly_price: Mapped[float] = mapped_column(Numeric(10, 2), default=0.00)
    max_users: Mapped[int] = mapped_column(default=1)
    max_branches: Mapped[int] = mapped_column(default=1)
    is_active: Mapped[bool] = mapped_column(default=True)
    features: Mapped[str] = mapped_column(Text, nullable=True)  # JSON features
    
    # Module permissions
    can_access_purchases: Mapped[bool] = mapped_column(default=False)
    can_access_inventory: Mapped[bool] = mapped_column(default=False)
    can_access_accounting: Mapped[bool] = mapped_column(default=False)
    can_access_assets: Mapped[bool] = mapped_column(default=False)
    can_access_manufacturing: Mapped[bool] = mapped_column(default=False)
    can_access_projects: Mapped[bool] = mapped_column(default=False)
    can_access_financial_dimensions: Mapped[bool] = mapped_column(default=False)
    can_access_printing: Mapped[bool] = mapped_column(default=False)
    
    # Document limits
    max_documents_per_month: Mapped[int] = mapped_column(default=100)
    can_print_documents: Mapped[bool] = mapped_column(default=True)
