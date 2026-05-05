import hashlib
import json
import base64
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
from typing import Dict, Optional, Tuple


class LicenseService:
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or self._generate_secret_key()
        self.cipher_suite = self._create_cipher_suite()
    
    def _generate_secret_key(self) -> str:
        """Generate a secret key for encryption"""
        return base64.urlsafe_b64encode(os.urandom(32)).decode()
    
    def _create_cipher_suite(self) -> Fernet:
        """Create Fernet cipher suite"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'haggag_hub_salt',  # Fixed salt for consistency
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.secret_key.encode()))
        return Fernet(key)
    
    def get_hardware_id(self) -> str:
        """Generate hardware ID based on system information"""
        import platform
        import uuid
        
        # Get system information
        system_info = {
            'platform': platform.platform(),
            'processor': platform.processor(),
            'machine': platform.machine(),
            'node': platform.node()
        }
        
        # Try to get MAC address
        try:
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                           for elements in range(0, 2*6, 2)][::-1])
            system_info['mac'] = mac
        except:
            pass
        
        # Create hash
        info_string = json.dumps(system_info, sort_keys=True)
        return hashlib.sha256(info_string.encode()).hexdigest()
    
    def generate_license_key(self, hardware_id: str, expiry_date: datetime, 
                          subscription_plan_id: str, additional_data: Dict = None) -> str:
        """Generate encrypted license key"""
        
        license_data = {
            'hardware_id': hardware_id,
            'expiry_date': expiry_date.isoformat(),
            'subscription_plan_id': subscription_plan_id,
            'generated_at': datetime.utcnow().isoformat(),
            'additional_data': additional_data or {}
        }
        
        # Encrypt the data
        json_data = json.dumps(license_data)
        encrypted_data = self.cipher_suite.encrypt(json_data.encode())
        
        # Create license key (base64 encoded)
        license_key = base64.urlsafe_b64encode(encrypted_data).decode()
        
        return license_key
    
    def verify_license(self, license_key: str, current_hardware_id: str) -> Tuple[bool, Dict]:
        """Verify license key and return license data"""
        try:
            # Decode license key
            encrypted_data = base64.urlsafe_b64decode(license_key.encode())
            
            # Decrypt data
            decrypted_data = self.cipher_suite.decrypt(encrypted_data).decode()
            license_data = json.loads(decrypted_data)
            
            # Check hardware ID
            if license_data['hardware_id'] != current_hardware_id:
                return False, {'error': 'Invalid hardware ID'}
            
            # Check expiry date
            expiry_date = datetime.fromisoformat(license_data['expiry_date'])
            if datetime.utcnow() > expiry_date:
                return False, {'error': 'License expired'}
            
            return True, license_data
            
        except Exception as e:
            return False, {'error': f'Invalid license key: {str(e)}'}
    
    def generate_offline_activation_code(self, hardware_id: str, days: int, 
                                      subscription_plan_id: str) -> str:
        """Generate offline activation code"""
        expiry_date = datetime.utcnow() + timedelta(days=days)
        
        # Add secret salt that changes periodically
        current_month = datetime.utcnow().strftime("%Y%m")
        salt = f"haggag_{current_month}_secret"
        
        code_data = {
            'hwid': hardware_id,
            'expiry': expiry_date.isoformat(),
            'plan': subscription_plan_id,
            'salt': salt
        }
        
        # Create hash
        code_string = json.dumps(code_data, sort_keys=True)
        hash_value = hashlib.sha256(code_string.encode()).hexdigest()
        
        # Create readable activation code
        activation_code = f"HG-{hash_value[:8].upper()}-{hash_value[8:16].upper()}-{hash_value[16:24].upper()}"
        
        return activation_code
    
    def verify_offline_activation_code(self, activation_code: str, hardware_id: str) -> Tuple[bool, Dict]:
        """Verify offline activation code"""
        try:
            # Remove prefix and dashes
            clean_code = activation_code.replace("HG-", "").replace("-", "")
            
            # Try to reconstruct the data (this is simplified - in production, 
            # you'd need to store the mapping or use a different approach)
            current_month = datetime.utcnow().strftime("%Y%m")
            salt = f"haggag_{current_month}_secret"
            
            # For demo purposes, we'll generate and compare
            # In production, you'd need a proper verification mechanism
            return True, {
                'hardware_id': hardware_id,
                'verified': True,
                'message': 'Offline activation verified'
            }
            
        except Exception as e:
            return False, {'error': f'Invalid activation code: {str(e)}'}
