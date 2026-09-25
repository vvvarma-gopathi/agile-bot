from sqlalchemy import (Column,String,Boolean,Integer,DateTime,func,Text,ForeignKey)
from sqlalchemy.orm import declarative_base
from core.database import Base
from sqlalchemy.types import UUID
import uuid

class Roles(Base):

    __tablename__='roles'

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,unique=True,nullable=False)
    description=Column(Text,nullable=False)

class Users(Base):
    __tablename__="users"

    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    user_name=Column(String(30),unique=True,nullable=False)
    hashed_password=Column(String(300),nullable=False)
    name=Column(String(100),nullable=False)
    email=Column(String(225),unique=True,nullable=False)
    phone_number=Column(String(14),unique=True,nullable=False)
    role_id=Column(Integer,ForeignKey('roles.id',ondelete='CASCADE'),nullable=False)
    is_active=Column(Boolean,default=True,nullable=False)
    is_deleted=Column(Boolean,default=False,nullable=False)
    updated_at=Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)

