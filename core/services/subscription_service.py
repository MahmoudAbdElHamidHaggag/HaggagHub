from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from core.models.entities.subscription_plan import SubscriptionPlan
from core.models.entities.tenant import Tenant


class SubscriptionService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_subscription_plan(self, plan_data: Dict) -> SubscriptionPlan:
        """Create new subscription plan"""
        plan = SubscriptionPlan(
            name=plan_data['name'],
            code=plan_data['code'],
            description=plan_data.get('description'),
            monthly_price=plan_data.get('monthly_price', 0.00),
            yearly_price=plan_data.get('yearly_price', 0.00),
            max_users=plan_data.get('max_users', 1),
            max_branches=plan_data.get('max_branches', 1),
            features=plan_data.get('features'),
            can_access_purchases=plan_data.get('can_access_purchases', False),
            can_access_inventory=plan_data.get('can_access_inventory', False),
            can_access_accounting=plan_data.get('can_access_accounting', False),
            can_access_assets=plan_data.get('can_access_assets', False),
            can_access_manufacturing=plan_data.get('can_access_manufacturing', False),
            can_access_projects=plan_data.get('can_access_projects', False),
            can_access_financial_dimensions=plan_data.get('can_access_financial_dimensions', False),
            can_access_printing=plan_data.get('can_access_printing', True),
            max_documents_per_month=plan_data.get('max_documents_per_month', 100),
            can_print_documents=plan_data.get('can_print_documents', True)
        )
        
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        
        return plan
    
    def get_all_plans(self, active_only: bool = True) -> List[SubscriptionPlan]:
        """Get all subscription plans"""
        query = self.db.query(SubscriptionPlan)
        if active_only:
            query = query.filter(SubscriptionPlan.is_active == True)
        return query.all()
    
    def get_plan_by_id(self, plan_id: str) -> Optional[SubscriptionPlan]:
        """Get subscription plan by ID"""
        return self.db.query(SubscriptionPlan).filter(SubscriptionPlan.id == plan_id).first()
    
    def get_plan_by_code(self, code: str) -> Optional[SubscriptionPlan]:
        """Get subscription plan by code"""
        return self.db.query(SubscriptionPlan).filter(SubscriptionPlan.code == code).first()
    
    def update_plan(self, plan_id: str, update_data: Dict) -> SubscriptionPlan:
        """Update subscription plan"""
        plan = self.get_plan_by_id(plan_id)
        if not plan:
            raise ValueError("Subscription plan not found")
        
        # Update allowed fields
        allowed_fields = [
            'name', 'description', 'monthly_price', 'yearly_price',
            'max_users', 'max_branches', 'features', 'is_active',
            'can_access_purchases', 'can_access_inventory', 'can_access_accounting',
            'can_access_assets', 'can_access_manufacturing', 'can_access_projects',
            'can_access_financial_dimensions', 'can_access_printing',
            'max_documents_per_month', 'can_print_documents'
        ]
        
        for field, value in update_data.items():
            if field in allowed_fields and hasattr(plan, field):
                setattr(plan, field, value)
        
        self.db.commit()
        self.db.refresh(plan)
        
        return plan
    
    def delete_plan(self, plan_id: str) -> bool:
        """Delete subscription plan (soft delete by setting is_active=False)"""
        plan = self.get_plan_by_id(plan_id)
        if not plan:
            return False
        
        plan.is_active = False
        self.db.commit()
        
        return True
    
    def upgrade_tenant_plan(self, tenant_id: str, new_plan_id: str, 
                          billing_cycle: str = 'monthly') -> Tenant:
        """Upgrade tenant to new subscription plan"""
        tenant = self.db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if not tenant:
            raise ValueError("Tenant not found")
        
        new_plan = self.get_plan_by_id(new_plan_id)
        if not new_plan:
            raise ValueError("Subscription plan not found")
        
        # Update tenant subscription
        tenant.subscription_plan_id = new_plan_id
        
        # Calculate new expiry date
        if billing_cycle == 'monthly':
            tenant.subscription_expiry = datetime.utcnow() + timedelta(days=30)
        elif billing_cycle == 'yearly':
            tenant.subscription_expiry = datetime.utcnow() + timedelta(days=365)
        
        self.db.commit()
        self.db.refresh(tenant)
        
        return tenant
    
    def get_plan_comparison(self) -> List[Dict]:
        """Get comparison of all active plans"""
        plans = self.get_all_plans(active_only=True)
        
        comparison = []
        for plan in plans:
            comparison.append({
                'id': plan.id,
                'name': plan.name,
                'code': plan.code,
                'monthly_price': float(plan.monthly_price),
                'yearly_price': float(plan.yearly_price),
                'max_users': plan.max_users,
                'max_branches': plan.max_branches,
                'features': {
                    'purchases': plan.can_access_purchases,
                    'inventory': plan.can_access_inventory,
                    'accounting': plan.can_access_accounting,
                    'assets': plan.can_access_assets,
                    'manufacturing': plan.can_access_manufacturing,
                    'projects': plan.can_access_projects,
                    'financial_dimensions': plan.can_access_financial_dimensions,
                    'printing': plan.can_access_printing
                },
                'limits': {
                    'max_documents_per_month': plan.max_documents_per_month,
                    'can_print_documents': plan.can_print_documents
                }
            })
        
        return comparison
    
    def get_usage_stats(self, tenant_id: str) -> Dict:
        """Get tenant usage statistics"""
        tenant = self.db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if not tenant:
            return {}
        
        plan = self.get_plan_by_id(tenant.subscription_plan_id) if tenant.subscription_plan_id else None
        if not plan:
            return {}
        
        # Get current usage (this would need actual implementation based on your business logic)
        current_usage = {
            'users_count': 1,  # This should be calculated from actual users
            'branches_count': 1,  # This should be calculated from actual branches
            'documents_this_month': 50  # This should be calculated from actual documents
        }
        
        return {
            'plan_limits': {
                'max_users': plan.max_users,
                'max_branches': plan.max_branches,
                'max_documents_per_month': plan.max_documents_per_month
            },
            'current_usage': current_usage,
            'usage_percentage': {
                'users': (current_usage['users_count'] / plan.max_users) * 100 if plan.max_users > 0 else 0,
                'branches': (current_usage['branches_count'] / plan.max_branches) * 100 if plan.max_branches > 0 else 0,
                'documents': (current_usage['documents_this_month'] / plan.max_documents_per_month) * 100 if plan.max_documents_per_month > 0 else 0
            }
        }
