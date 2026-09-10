from sqlalchemy import Column,String,Boolean,Integer,DateTime,func
from sqlalchemy.orm import declarative_base

Base=declarative_base()

class Users(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    user_name=Column(String(30),unique=True,nullable=False)
    hashed_password=Column(String(300),nullable=False)
    name=Column(String(50),nullable=False)
    email=Column(String(225),unique=True,nullable=False)
    phone_number=Column(String(14),unique=True,nullable=False)
    role=Column(String(50),nullable=False,default="user")
    is_active=Column(Boolean,default=True,nullable=False)
    is_deleted=Column(Boolean,default=False,nullable=False)
    updated_at=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)