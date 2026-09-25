from core.database import Base
from sqlalchemy import (Column,Text,String,ForeignKey,func,DateTime,Integer,DECIMAL,Date)
from sqlalchemy.types import UUID
from uuid import uuid4


class Epics(Base):
    __tablename__='epics'
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    project_id=Column(UUID(as_uuid=True),ForeignKey('projects.id',ondelete="CASCADE"),default=uuid4,nullable=False)
    title=Column(String(225),nullable=False,unique=True)
    description=Column(Text,nullable=False)
    status=Column(String(20),nullable=False)
    priority=Column(String(20),nullable=False)
    created_by=Column(UUID(as_uuid=True),ForeignKey('users.id',ondelete="CASCADE"),nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now(),nullable=False,)
    updated_at = Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)


class UserStories(Base):
    __tablename__='user_stories'
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    epic_id=Column(UUID(as_uuid=True),ForeignKey('epics.id',ondelete="CASCADE"),nullable=False)
    title=Column(String(225),nullable=False,unique=True)
    description=Column(Text,nullable=False)
    acceptance_criteria=Column(Text,nullable=False)
    priority=Column(String(20),nullable=False)
    story_points=Column(Integer,nullable=False)
    status=Column(String(20),nullable=False)
    created_by=Column(UUID(as_uuid=True),ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at=Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)

class Tasks(Base):
    __tablename__='tasks'
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    user_story_id=Column(UUID(as_uuid=True),ForeignKey('user_stories.id',ondelete="CASCADE"),default=uuid4,nullable=False)
    project_id=Column(UUID(as_uuid=True),ForeignKey('projects.id',ondelete="CASCADE"),default=uuid4,nullable=False)
    title=Column(String(225),nullable=False,unique=True)
    description=Column(Text,nullable=False)
    priority=Column(String(20),nullable=False)
    status=Column(String(20),nullable=False)
    assigned_to=Column(UUID(as_uuid=True),ForeignKey("users.id",ondelete="CASCADE"),nullable=True)
    created_by=Column(UUID(as_uuid=True),ForeignKey('users.id',ondelete="CASCADE"),default=uuid4,nullable=False)
    estimated_hours=Column(DECIMAL(6,2),nullable=False)
    actual_hours=Column(DECIMAL(6,2),nullable=False)
    due_date=Column(Date,nullable=False)
    completed_at=Column(DateTime(timezone=True),nullable=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at=Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)
    

class TaskDependencies(Base):
    __tablename__='task_dependencies'
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    task_id=Column(UUID(as_uuid=True),ForeignKey('tasks.id'),nullable=False)
    depends_on_task_id=Column(UUID(as_uuid=True),ForeignKey('tasks.id'),nullable=False)
    dependency_type=Column(String(20),nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)