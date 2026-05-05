from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime


class LicenseVerify(BaseModel):
    hardware_id: str
    license_key: str


class LicenseGenerate(BaseModel):
    tenant_id: str
    days: Optional[int] = 30


class LicenseActivate(BaseModel):
    tenant_id: str
    hardware_id: str
    license_key: str


class LicenseResponse(BaseModel):
    id: str
    tenant_id: str
    hardware_id: str
    license_key: str
    is_active: bool
    issued_at: datetime
    expires_at: datetime
    last_verified: Optional[datetime] = None
    verification_count: int
    is_online_license: bool
    subscription_plan_id: Optional[str] = None

    class Config:
        from_attributes = True


class LicenseVerificationResponse(BaseModel):
    success: bool
    data: Dict


class LicenseGenerationResponse(BaseModel):
    success: bool
    data: Dict


class LicenseActivationResponse(BaseModel):
    success: bool
    message: str
