from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import Dict

from database.session import get_db
from core.services.auth_service import AuthService
from core.schemas.auth import UserLogin, LoginResponse, ChangePassword, ResetPassword

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()


def get_current_user(credentials: str = Depends(security), db: Session = Depends(get_db)) -> Dict:
    """Get current user from token"""
    auth_service = AuthService(db)
    token = credentials.credentials
    user = auth_service.get_current_user_from_token(token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


@router.post("/login", response_model=LoginResponse)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return access token"""
    auth_service = AuthService(db)
    result = auth_service.login_user(
        username=user_credentials.username,
        password=user_credentials.password,
        tenant_code=user_credentials.tenant_code
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result["message"]
        )
    
    return result


@router.post("/change-password")
async def change_password(
    password_data: ChangePassword,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    auth_service = AuthService(db)
    success = auth_service.change_password(
        user_id=current_user.id,
        old_password=password_data.old_password,
        new_password=password_data.new_password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to change password. Please check your old password."
        )
    
    return {"success": True, "message": "Password changed successfully"}


@router.post("/reset-password")
async def reset_password(
    password_data: ResetPassword,
    user_id: str,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reset user password (admin only)"""
    # Check if current user is admin
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can reset passwords"
        )
    
    auth_service = AuthService(db)
    success = auth_service.reset_password(
        user_id=user_id,
        new_password=password_data.new_password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"success": True, "message": "Password reset successfully"}


@router.get("/me")
async def get_current_user_info(current_user: Dict = Depends(get_current_user)):
    """Get current user information"""
    return {
        "success": True,
        "data": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "role": current_user.role,
            "tenant_id": current_user.tenant_id,
            "is_active": current_user.is_active
        }
    }
