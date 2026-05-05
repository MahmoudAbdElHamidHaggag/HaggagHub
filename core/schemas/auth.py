from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[str] = "user"


class UserCreate(UserBase):
    password: str
    tenant_id: str


class UserLogin(BaseModel):
    username: str
    password: str
    tenant_code: Optional[str] = None


class UserResponse(UserBase):
    id: str
    tenant_id: str
    is_active: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[str] = None
    tenant_id: Optional[str] = None
    tenant_code: Optional[str] = None
    role: Optional[str] = None


class LoginResponse(BaseModel):
    success: bool
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    user: Optional[UserResponse] = None
    tenant: Optional[dict] = None
    message: Optional[str] = None


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class ResetPassword(BaseModel):
    new_password: str
