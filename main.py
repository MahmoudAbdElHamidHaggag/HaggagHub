from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
import uvicorn

from database.session import get_db
from core.services.tenant_service import TenantService
from core.services.subscription_service import SubscriptionService
from core.services.license_service import LicenseService
from core.services.sync_service import SyncService
from core.services.auth_service import AuthService
from config import settings
from api.v1.auth import router as auth_router

app = FastAPI(
    title="HaggagHub ERP API",
    description="Multi-tenant ERP System with Offline/Online Sync",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/v1")

# Security
security = HTTPBearer()

def get_current_tenant(credentials: HTTPAuthorizationCredentials = Depends(security), 
                       db: Session = Depends(get_db)) -> Dict:
    """Get current tenant from token"""
    auth_service = AuthService(db)
    token = credentials.credentials
    user = auth_service.get_current_user_from_token(token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"tenant_id": user.tenant_id, "user_id": user.id, "user": user}

# Tenant endpoints
@app.post("/api/v1/tenants")
async def create_tenant(tenant_data: Dict, db: Session = Depends(get_db)):
    """Create new tenant"""
    try:
        tenant_service = TenantService(db)
        tenant = tenant_service.create_tenant(tenant_data)
        return {"success": True, "data": tenant}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/tenants/{tenant_id}")
async def get_tenant(tenant_id: str, db: Session = Depends(get_db)):
    """Get tenant by ID"""
    tenant_service = TenantService(db)
    tenant = tenant_service.get_tenant_by_id(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return {"success": True, "data": tenant}

@app.get("/api/v1/tenants/{tenant_id}/subscription-status")
async def get_subscription_status(tenant_id: str, db: Session = Depends(get_db)):
    """Get tenant subscription status"""
    tenant_service = TenantService(db)
    status = tenant_service.check_subscription_status(tenant_id)
    return {"success": True, "data": status}

@app.get("/api/v1/tenants/{tenant_id}/features")
async def get_tenant_features(tenant_id: str, db: Session = Depends(get_db)):
    """Get tenant available features"""
    tenant_service = TenantService(db)
    features = tenant_service.get_tenant_features(tenant_id)
    return {"success": True, "data": features}

# Subscription endpoints
@app.post("/api/v1/subscription-plans")
async def create_subscription_plan(plan_data: Dict, db: Session = Depends(get_db)):
    """Create new subscription plan"""
    try:
        subscription_service = SubscriptionService(db)
        plan = subscription_service.create_subscription_plan(plan_data)
        return {"success": True, "data": plan}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/subscription-plans")
async def get_subscription_plans(active_only: bool = True, db: Session = Depends(get_db)):
    """Get all subscription plans"""
    subscription_service = SubscriptionService(db)
    plans = subscription_service.get_all_plans(active_only)
    return {"success": True, "data": plans}

@app.get("/api/v1/subscription-plans/comparison")
async def get_plan_comparison(db: Session = Depends(get_db)):
    """Get comparison of all plans"""
    subscription_service = SubscriptionService(db)
    comparison = subscription_service.get_plan_comparison()
    return {"success": True, "data": comparison}

# License endpoints
@app.post("/api/v1/licenses/verify")
async def verify_license(license_data: Dict, db: Session = Depends(get_db)):
    """Verify license key"""
    try:
        license_service = LicenseService()
        hardware_id = license_data.get('hardware_id')
        license_key = license_data.get('license_key')
        
        is_valid, result = license_service.verify_license(license_key, hardware_id)
        
        return {
            "success": True,
            "data": {
                "is_valid": is_valid,
                "result": result
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/licenses/generate-offline")
async def generate_offline_license(request_data: Dict, db: Session = Depends(get_db)):
    """Generate offline license for tenant"""
    try:
        tenant_id = request_data.get('tenant_id')
        days = request_data.get('days', 30)
        
        tenant_service = TenantService(db)
        license_key = tenant_service.generate_offline_license(tenant_id, days)
        
        return {"success": True, "data": {"license_key": license_key}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/licenses/activate-offline")
async def activate_offline_license(activation_data: Dict, db: Session = Depends(get_db)):
    """Activate offline license"""
    try:
        tenant_id = activation_data.get('tenant_id')
        hardware_id = activation_data.get('hardware_id')
        license_key = activation_data.get('license_key')
        
        tenant_service = TenantService(db)
        success = tenant_service.activate_offline_license(tenant_id, hardware_id, license_key)
        
        if success:
            return {"success": True, "message": "License activated successfully"}
        else:
            return {"success": False, "message": "License activation failed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Sync endpoints
@app.get("/api/v1/sync/status")
async def get_sync_status(tenant: Dict = Depends(get_current_tenant), 
                         db: Session = Depends(get_db)):
    """Get sync status"""
    try:
        sync_service = SyncService(db, tenant['tenant_id'])
        status = sync_service.get_sync_status()
        return {"success": True, "data": status}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/sync/upload")
async def sync_upload(sync_data: Dict, 
                      tenant: Dict = Depends(get_current_tenant),
                      db: Session = Depends(get_db)):
    """Upload data to online server"""
    try:
        sync_service = SyncService(db, tenant['tenant_id'])
        result = sync_service.sync_to_online(sync_data)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/sync/download")
async def sync_download(request_data: Dict,
                       tenant: Dict = Depends(get_current_tenant),
                       db: Session = Depends(get_db)):
    """Download data from online server"""
    try:
        sync_service = SyncService(db, tenant['tenant_id'])
        model_name = request_data.get('model')
        model_class = sync_service._get_model_class(model_name)
        
        if not model_class:
            raise HTTPException(status_code=400, detail="Invalid model name")
        
        result = sync_service.sync_from_online(model_class)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Health check
@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "1.0.0"
    }

# System info
@app.get("/api/v1/system/info")
async def get_system_info():
    """Get system information"""
    return {
        "app_name": "HaggagHub ERP",
        "version": "1.0.0",
        "mode": settings.APP_MODE,
        "database_url": settings.LOCAL_DB_URL if settings.APP_MODE == "AUTO" else "Online Database"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True
    )
