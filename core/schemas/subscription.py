from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime


class SubscriptionPlanBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    monthly_price: Optional[float] = 0.00
    yearly_price: Optional[float] = 0.00
    max_users: Optional[int] = 1
    max_branches: Optional[int] = 1
    features: Optional[str] = None
    can_access_purchases: Optional[bool] = False
    can_access_inventory: Optional[bool] = False
    can_access_accounting: Optional[bool] = False
    can_access_assets: Optional[bool] = False
    can_access_manufacturing: Optional[bool] = False
    can_access_projects: Optional[bool] = False
    can_access_financial_dimensions: Optional[bool] = False
    can_access_printing: Optional[bool] = True
    max_documents_per_month: Optional[int] = 100
    can_print_documents: Optional[bool] = True


class SubscriptionPlanCreate(SubscriptionPlanBase):
    pass


class SubscriptionPlanUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    monthly_price: Optional[float] = None
    yearly_price: Optional[float] = None
    max_users: Optional[int] = None
    max_branches: Optional[int] = None
    features: Optional[str] = None
    is_active: Optional[bool] = None
    can_access_purchases: Optional[bool] = None
    can_access_inventory: Optional[bool] = None
    can_access_accounting: Optional[bool] = None
    can_access_assets: Optional[bool] = None
    can_access_manufacturing: Optional[bool] = None
    can_access_projects: Optional[bool] = None
    can_access_financial_dimensions: Optional[bool] = None
    can_access_printing: Optional[bool] = None
    max_documents_per_month: Optional[int] = None
    can_print_documents: Optional[bool] = None


class SubscriptionPlanResponse(SubscriptionPlanBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PlanComparison(BaseModel):
    id: str
    name: str
    code: str
    monthly_price: float
    yearly_price: float
    max_users: int
    max_branches: int
    features: Dict[str, bool]
    limits: Dict[str, int]


class UsageStats(BaseModel):
    plan_limits: Dict[str, int]
    current_usage: Dict[str, int]
    usage_percentage: Dict[str, float]
