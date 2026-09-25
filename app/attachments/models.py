from core.database import Base
from sqlalchemy import Column,UUID,ForeignKey,func,String,Text,Boolean,DateTime,BIGINT
from uuid import uuid4
class Comments(Base):
    __tablename__='comments'
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    user_id=Column(UUID(as_uuid=True),ForeignKey('users.id',ondelete="CASCADE"),nullable=False)
    task_id=Column(UUID(as_uuid=True),ForeignKey('tasks.id',ondelete="CASCADE"),nullable=False)
    project_id=Column(UUID(as_uuid=True),ForeignKey('projects.id',ondelete="CASCADE"),nullable=False)
    parent_comment_id=Column(UUID(as_uuid=True),ForeignKey('comments.id',ondelete='CASCADE'),nullable=True)
    content=Column(Text,nullable=False)
    is_delete=Column(Boolean,nullable=False,default=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at=Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=True)

class Attachments(Base):
    __tablename__='attachments'
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    uploaded_by=Column(UUID(as_uuid=True),ForeignKey('users.id',ondelete="CASCADE"),nullable=False)
    task_id=Column(UUID(as_uuid=True),ForeignKey('tasks.id',ondelete="CASCADE"),nullable=False)
    comment_id=Column(UUID(as_uuid=True),ForeignKey('comments.id',ondelete="CASCADE"),nullable=False)
    file_name=Column(String(225),nullable=False)
    file_type=Column(String(100),nullable=False)
    file_url=Column(Text,nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    
