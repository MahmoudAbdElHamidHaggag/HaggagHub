from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from core.models.entities.tenant import Tenant
from core.models.entities.subscription_plan import SubscriptionPlan
from core.models.entities.license import License
from core.services.license_service import LicenseService


class TenantService:
    def __init__(self, db: Session):
        self.db = db
        self.license_service = LicenseService()
    
    def create_tenant(self, tenant_data: Dict, subscription_plan_id: str = None) -> Tenant:
        """Create new tenant"""
        tenant = Tenant(
            name=tenant_data['name'],
            code=tenant_data['code'],
            domain=tenant_data.get('domain'),
            contact_email=tenant_data.get('contact_email'),
            contact_phone=tenant_data.get('contact_phone'),
            address=tenant_data.get('address'),
            currency_code=tenant_data.get('currency_code', 'EGP'),
            subscription_plan_id=subscription_plan_id,
            is_online_mode=tenant_data.get('is_online_mode', True)
        )
        
        self.db.add(tenant)
        self.db.commit()
        self.db.refresh(tenant)
        
        return tenant
    
    def get_tenant_by_id(self, tenant_id: str) -> Optional[Tenant]:
        """Get tenant by ID"""
        return self.db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    def get_tenant_by_code(self, code: str) -> Optional[Tenant]:
        """Get tenant by code"""
        return self.db.query(Tenant).filter(Tenant.code == code).first()
    
    def update_tenant_subscription(self, tenant_id: str, subscription_plan_id: str, 
                                 expiry_date: datetime = None) -> Tenant:
        """Update tenant subscription"""
        tenant = self.get_tenant_by_id(tenant_id)
        if not tenant:
            raise ValueError("Tenant not found")
        
        tenant.subscription_plan_id = subscription_plan_id
        if expiry_date:
            tenant.subscription_expiry = expiry_date
        
        self.db.commit()
        self.db.refresh(tenant)
        
        return tenant
    
    def activate_offline_license(self, tenant_id: str, hardware_id: str, 
                              license_key: str) -> bool:
        """Activate offline license for tenant"""
        tenant = self.get_tenant_by_id(tenant_id)
        if not tenant:
            raise ValueError("Tenant not found")
        
        # Verify license
        is_valid, license_data = self.license_service.verify_license(license_key, hardware_id)
        
        if not is_valid:
            return False
        
        # Update tenant with license info
        tenant.hardware_id = hardware_id
        tenant.license_key = license_key
        tenant.is_online_mode = False
        tenant.subscription_expiry = datetime.fromisoformat(license_data['expiry_date'])
        tenant.subscription_plan_id = license_data['subscription_plan_id']
        
        # Create license record
        license_record = License(
            tenant_id=tenant_id,
            hardware_id=hardware_id,
            license_key=license_key,
            encrypted_data=license_key,  # Store encrypted data
            expires_at=datetime.fromisoformat(license_data['expiry_date']),
            is_online_license=False,
            subscription_plan_id=license_data['subscription_plan_id']
        )
        
        self.db.add(license_record)
        self.db.commit()
        
        return True
    
    def check_subscription_status(self, tenant_id: str) -> Dict:
        """Check tenant subscription status"""
        tenant = self.get_tenant_by_id(tenant_id)
        if not tenant:
            return {'status': 'error', 'message': 'Tenant not found'}
        
        # Check subscription expiry
        if tenant.subscription_expiry and datetime.utcnow() > tenant.subscription_expiry:
            return {
                'status': 'expired',
                'message': 'Subscription expired',
                'expiry_date': tenant.subscription_expiry
            }
        
        # Get subscription plan details
        plan = None
        if tenant.subscription_plan_id:
            plan = self.db.query(SubscriptionPlan).filter(
                SubscriptionPlan.id == tenant.subscription_plan_id
            ).first()
        
        return {
            'status': 'active',
            'plan': plan.name if plan else None,
            'expiry_date': tenant.subscription_expiry,
            'is_online_mode': tenant.is_online_mode
        }
    
    def get_tenant_features(self, tenant_id: str) -> Dict:
        """Get tenant available features based on subscription plan"""
        tenant = self.get_tenant_by_id(tenant_id)
        if not tenant:
            return {}
        
        # Get subscription plan
        plan = None
        if tenant.subscription_plan_id:
            plan = self.db.query(SubscriptionPlan).filter(
                SubscriptionPlan.id == tenant.subscription_plan_id
            ).first()
        
        if not plan:
            return {}
        
        return {
            'max_users': plan.max_users,
            'max_branches': plan.max_branches,
            'can_access_purchases': plan.can_access_purchases,
            'can_access_inventory': plan.can_access_inventory,
            'can_access_accounting': plan.can_access_accounting,
            'can_access_assets': plan.can_access_assets,
            'can_access_manufacturing': plan.can_access_manufacturing,
            'can_access_projects': plan.can_access_projects,
            'can_access_financial_dimensions': plan.can_access_financial_dimensions,
            'can_access_printing': plan.can_access_printing,
            'max_documents_per_month': plan.max_documents_per_month,
            'can_print_documents': plan.can_print_documents
        }
    
    def generate_offline_license(self, tenant_id: str, days: int) -> str:
        """Generate offline license for tenant"""
        tenant = self.get_tenant_by_id(tenant_id)
        if not tenant:
            raise ValueError("Tenant not found")
        
        hardware_id = self.license_service.get_hardware_id()
        
        if not tenant.subscription_plan_id:
            raise ValueError("No subscription plan found")
        
        license_key = self.license_service.generate_license_key(
            hardware_id=hardware_id,
            expiry_date=datetime.utcnow() + timedelta(days=days),
            subscription_plan_id=tenant.subscription_plan_id,
            additional_data={
                'tenant_name': tenant.name,
                'tenant_code': tenant.code
            }
        )
        
        return license_key
