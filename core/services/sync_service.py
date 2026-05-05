from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
from datetime import datetime
import json
from core.models.base.abstract_base import AbstractBaseModel


class SyncService:
    def __init__(self, db: Session, tenant_id: str):
        self.db = db
        self.tenant_id = tenant_id
    
    def get_pending_sync_records(self, model_class: type, limit: int = 100) -> List[AbstractBaseModel]:
        """Get records that need to be synced"""
        return self.db.query(model_class).filter(
            model_class.tenant_id == self.tenant_id,
            model_class.is_synced == False
        ).limit(limit).all()
    
    def mark_as_synced(self, model_class: type, record_ids: List[str]) -> bool:
        """Mark records as synced"""
        try:
            self.db.query(model_class).filter(
                model_class.id.in_(record_ids),
                model_class.tenant_id == self.tenant_id
            ).update({'is_synced': True}, synchronize_session=False)
            
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error marking records as synced: {e}")
            return False
    
    def sync_to_online(self, sync_data: Dict) -> Dict:
        """Sync data to online server"""
        try:
            # This would make HTTP request to online server
            # For now, return success response
            return {
                'success': True,
                'synced_records': len(sync_data.get('records', [])),
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def sync_from_online(self, model_class: type, last_sync_time: datetime = None) -> Dict:
        """Sync data from online server"""
        try:
            # This would fetch data from online server
            # For now, return empty response
            return {
                'success': True,
                'records': [],
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def resolve_conflicts(self, local_record: AbstractBaseModel, 
                         online_record: Dict) -> AbstractBaseModel:
        """Resolve conflicts between local and online records"""
        # Simple strategy: use the most recently updated record
        if online_record.get('updated_at') > local_record.updated_at:
            # Update local record with online data
            for key, value in online_record.items():
                if hasattr(local_record, key) and key not in ['id', 'tenant_id', 'created_at']:
                    setattr(local_record, key, value)
            
            local_record.updated_at = datetime.utcnow()
            local_record.is_synced = True
        
        return local_record
    
    def get_sync_status(self) -> Dict:
        """Get overall sync status"""
        # Get counts for each model type
        status = {
            'pending_sync': {},
            'last_sync': None,
            'total_records': {}
        }
        
        # Check each model type
        model_types = [
            'Item', 'Warehouse', 'PurchaseOrder', 'JournalEntry',
            'ChartOfAccounts', 'CostCenter', 'Project'
        ]
        
        for model_name in model_types:
            try:
                model_class = self._get_model_class(model_name)
                if model_class:
                    pending_count = self.db.query(model_class).filter(
                        model_class.tenant_id == self.tenant_id,
                        model_class.is_synced == False
                    ).count()
                    
                    total_count = self.db.query(model_class).filter(
                        model_class.tenant_id == self.tenant_id
                    ).count()
                    
                    status['pending_sync'][model_name] = pending_count
                    status['total_records'][model_name] = total_count
            except Exception as e:
                print(f"Error getting sync status for {model_name}: {e}")
        
        return status
    
    def _get_model_class(self, model_name: str):
        """Get model class by name"""
        try:
            from core.models.entities import (
                Item, Warehouse, PurchaseOrder, JournalEntry,
                ChartOfAccounts, CostCenter, Project
            )
            
            model_map = {
                'Item': Item,
                'Warehouse': Warehouse,
                'PurchaseOrder': PurchaseOrder,
                'JournalEntry': JournalEntry,
                'ChartOfAccounts': ChartOfAccounts,
                'CostCenter': CostCenter,
                'Project': Project
            }
            
            return model_map.get(model_name)
        except ImportError:
            return None
    
    def create_sync_batch(self, model_class: type, batch_size: int = 50) -> Dict:
        """Create a batch of records for syncing"""
        records = self.get_pending_sync_records(model_class, batch_size)
        
        if not records:
            return {'records': [], 'count': 0}
        
        batch_data = []
        for record in records:
            record_dict = {
                'id': record.id,
                'model': model_class.__name__,
                'data': self._model_to_dict(record),
                'operation': 'update' if record.created_at != record.updated_at else 'create'
            }
            batch_data.append(record_dict)
        
        return {
            'records': batch_data,
            'count': len(batch_data),
            'tenant_id': self.tenant_id
        }
    
    def _model_to_dict(self, record: AbstractBaseModel) -> Dict:
        """Convert model instance to dictionary"""
        result = {}
        for column in record.__table__.columns:
            value = getattr(record, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            result[column.name] = value
        return result
    
    def process_sync_response(self, sync_response: Dict) -> bool:
        """Process response from online sync"""
        if not sync_response.get('success'):
            return False
        
        # Mark synced records
        synced_ids = sync_response.get('synced_ids', [])
        if synced_ids:
            # This would need to be implemented per model type
            pass
        
        return True
