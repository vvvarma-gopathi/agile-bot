from sqlalchemy import (Date,Boolean,Column,ForeignKey,String,Text,DateTime,func)
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import UUID
from core.database import Base
import uuid


class Projects(Base):
    __tablename__='projects'
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    owner_id=Column(UUID(as_uuid=True),ForeignKey('users.id',ondelete="CASCADE"),default=uuid.uuid4)
    name=Column(String(225),unique=True,nullable=False)
    description=Column(Text,nullable=False)
    goal=Column(Text,nullable=False)
    status=Column(String(20),nullable=False)
    start_date=Column(Date,nullable=False)
    end_date=Column(Date,nullable=False)
    updated_at=Column(DateTime(timezone=True),server_default=func.now(),server_onupdate=func.now(),nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)   


class Project_members(Base):
    __tablename__='project_members'
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    project_id=Column(UUID(as_uuid=True),ForeignKey('projects.id',ondelete='CASCADE'),default=uuid.uuid4,nullable=False)
    user_id=Column(UUID(as_uuid=True),ForeignKey('users.id',ondelete="CASCADE"),default=uuid.uuid4,nullable=False)
    project_role=Column(String(50),nullable=False)
    joined_at=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    is_active=Column(Boolean,nullable=False,default=True)

class Milestones(Base):
    __tablename__="milestones"
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    project_id=Column(UUID(as_uuid=True),ForeignKey('projects.id',ondelete="CASCADE"),default=uuid.uuid4,nullable=False)
    name=Column(String(225),unique=True,nullable=False)
    description=Column(Text,nullable=False)
    due_date=Column(Date,nullable=False)
    status=Column(String(20),nullable=False)
    created_by=Column(UUID(as_uuid=True),ForeignKey('users.id',ondelete="CASCADE"),default=uuid.uuid4,nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at=Column(DateTime(timezone=True),server_default=func.now(),server_onupdate=func.now(),nullable=False)
