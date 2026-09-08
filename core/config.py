import os
from dotenv import load_dotenv

load_dotenv()

class Setting:
    DatabaseHost=os.getenv("DatabaseHost")
    DatabasePassword=os.getenv("DatabasePassword")
    DatabasePort=os.getenv("DatabasePort")
    DatabaseName=os.getenv("DatabaseName")
    DatabaseUser=os.getenv("DatabaseUser")

settings=Setting()