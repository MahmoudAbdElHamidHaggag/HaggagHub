from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from core.models.entities.user import User
from core.models.entities.tenant import Tenant
from config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.secret_key = settings.SECRET_KEY if hasattr(settings, 'SECRET_KEY') else "your-secret-key-here"
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash password"""
        return pwd_context.hash(password)
    
    def authenticate_user(self, username: str, password: str, tenant_code: str = None) -> Optional[User]:
        """Authenticate user"""
        query = self.db.query(User).filter(User.username == username)
        
        if tenant_code:
            # Join with tenant to verify tenant code
            query = query.join(Tenant).filter(Tenant.code == tenant_code)
        
        user = query.first()
        
        if not user or not self.verify_password(password, user.password):
            return None
        
        return user
    
    def create_access_token(self, data: Dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None
    
    def create_user(self, user_data: Dict, tenant_id: str) -> User:
        """Create new user"""
        hashed_password = self.get_password_hash(user_data['password'])
        
        user = User(
            username=user_data['username'],
            password=hashed_password,
            tenant_id=tenant_id,
            email=user_data.get('email'),
            full_name=user_data.get('full_name'),
            is_active=user_data.get('is_active', True),
            role=user_data.get('role', 'user')
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def login_user(self, username: str, password: str, tenant_code: str = None) -> Dict:
        """Login user and return token"""
        user = self.authenticate_user(username, password, tenant_code)
        
        if not user:
            return {
                "success": False,
                "message": "Invalid credentials"
            }
        
        if not user.is_active:
            return {
                "success": False,
                "message": "Account is inactive"
            }
        
        # Get tenant info
        tenant = self.db.query(Tenant).filter(Tenant.id == user.tenant_id).first()
        
        access_token = self.create_access_token(
            data={
                "sub": user.username,
                "user_id": user.id,
                "tenant_id": user.tenant_id,
                "tenant_code": tenant.code if tenant else None,
                "role": user.role
            }
        )
        
        return {
            "success": True,
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role
            },
            "tenant": {
                "id": tenant.id,
                "name": tenant.name,
                "code": tenant.code
            } if tenant else None
        }
    
    def get_current_user_from_token(self, token: str) -> Optional[User]:
        """Get current user from token"""
        payload = self.verify_token(token)
        
        if payload is None:
            return None
        
        user_id = payload.get("user_id")
        if user_id is None:
            return None
        
        user = self.db.query(User).filter(User.id == user_id).first()
        return user
    
    def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        """Change user password"""
        user = self.db.query(User).filter(User.id == user_id).first()
        
        if not user or not self.verify_password(old_password, user.password):
            return False
        
        user.password = self.get_password_hash(new_password)
        self.db.commit()
        
        return True
    
    def reset_password(self, user_id: str, new_password: str) -> bool:
        """Reset user password (admin function)"""
        user = self.db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return False
        
        user.password = self.get_password_hash(new_password)
        self.db.commit()
        
        return True
