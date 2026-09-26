from core.database import Base
from sqlalchemy import ForeignKey,Column,String,Text,Date,func,DateTime
from sqlalchemy.types import UUID
from uuid import uuid4


class SprintItems(Base):
    __tablename__='sprint_items'
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    sprint_id=Column(UUID(as_uuid=True),ForeignKey('sprints.id',ondelete="CASCADE"),nullable=False)
    task_id=Column(UUID(as_uuid=True),ForeignKey('tasks.id',ondelete="CASCADE"),nullable=False,default=uuid4)
    added_at=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)

class Sprints(Base):
    __tablename__='sprints'
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    project_id=Column(UUID(as_uuid=True),ForeignKey('projects.id',ondelete="CASCADE"),default=uuid4,nullable=False)
    name=Column(String(225),nullable=False,unique=True)
    goal=Column(Text,nullable=False)
    start_date=Column(Date,nullable=False)
    end_date=Column(Date,nullable=False)
    status=Column(String(20),nullable=False)
    created_by=Column(UUID(as_uuid=True),ForeignKey('users.id',ondelete="CASCADE"),nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at=Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)


