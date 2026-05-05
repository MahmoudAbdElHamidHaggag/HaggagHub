from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
from datetime import datetime


class TenantBase(BaseModel):
    name: str
    code: str
    domain: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    currency_code: Optional[str] = "EGP"
    is_online_mode: Optional[bool] = True


class TenantCreate(TenantBase):
    subscription_plan_id: Optional[str] = None


class TenantUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    currency_code: Optional[str] = None
    is_online_mode: Optional[bool] = None


class TenantResponse(TenantBase):
    id: str
    subscription_plan_id: Optional[str] = None
    subscription_expiry: Optional[datetime] = None
    license_key: Optional[str] = None
    hardware_id: Optional[str] = None
    is_active: bool
    settings: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TenantSubscriptionStatus(BaseModel):
    status: str
    plan: Optional[str] = None
    expiry_date: Optional[datetime] = None
    is_online_mode: bool


class TenantFeatures(BaseModel):
    max_users: int
    max_branches: int
    can_access_purchases: bool
    can_access_inventory: bool
    can_access_accounting: bool
    can_access_assets: bool
    can_access_manufacturing: bool
    can_access_projects: bool
    can_access_financial_dimensions: bool
    can_access_printing: bool
    max_documents_per_month: int
    can_print_documents: bool
