import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    LOCAL_DB_URL = os.getenv("LOCAL_DB_URL", "sqlite:///./local_db.sqlite")
    TENANT_DB_URL_TEMPLATE = os.getenv("TENANT_DB_URL_TEMPLATE")

    APP_MODE = os.getenv("APP_MODE", "AUTO")

    def get_database_url(self, tenant_name: str = None, is_online: bool = False):
        if is_online:
            if not tenant_name:
                raise ValueError("Tenant name required in CENTRAL mode")
            return self.TENANT_DB_URL_TEMPLATE.format(tenant_db=tenant_name)

        return self.LOCAL_DB_URL


settings = Settings()