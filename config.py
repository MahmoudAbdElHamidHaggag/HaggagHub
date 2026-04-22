import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    LOCAL_DB_URL: str = os.getenv("LOCAL_DB_URL")
    REMOTE_DB_URL: str = os.getenv("REMOTE_DB_URL") 
settings = Settings()