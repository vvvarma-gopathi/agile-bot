import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL=os.getenv("Database_URL")

settings=Settings()