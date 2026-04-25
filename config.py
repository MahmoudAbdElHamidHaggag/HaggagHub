import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

class Settings:
    # APP_MODE = os.getenv("APP_MODE", "LOCAL") 
    
    # LOCAL_DB_URL = os.getenv("LOCAL_DB_URL", "sqlite:///./local_db.sqlite")
    REMOTE_DB_URL = os.getenv("REMOTE_DB_URL")
    
    # @property
    # def DATABASE_URL(self):
    #     if self.APP_MODE == "CENTRAL":
    #         return self.REMOTE_DB_URL
    #     return self.LOCAL_DB_URL

    # def __init__(self):
    #     print(f"--- النظام يعمل في وضع: {self.APP_MODE} ---")
    #     if self.APP_MODE == "CENTRAL" and not self.REMOTE_DB_URL:
    #         print("❌ خطأ: أنت في وضع المركز ولكن REMOTE_DB_URL غير موجود في .env")

settings = Settings()