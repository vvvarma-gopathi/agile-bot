import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL:str=os.getenv("DATABASE_URL")
    JWT_SecretKey:str=os.getenv("JWT_SecretKey")
    JWT_Hashing_Algorithm:str=os.getenv("JWT_Hashing_Algorithm")


settings=Settings()