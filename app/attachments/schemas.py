from datetime import datetime
from pydantic import Field,BaseModel
from typing import Optional
from uuid import UUID

class CreateComment(BaseModel):
    task_id:UUID
    project_id:UUID
    parent_comment_id:Optional[UUID]=None
    content:str=Field(...,min_length=1)

class UpdateComment(BaseModel):
    content:Optional[str]=Field(None,min_length=1)

class CommentResponse(BaseModel):
    id:UUID
    user_id:UUID
    task_id:UUID
    project_id:UUID
    parent_comment_id:Optional[UUID]
    content:str
    is_delete:bool
    created_at:datetime
    updated_at:Optional[datetime]

class MessageResponse(BaseModel):
    message:str

class CreateAttachment(BaseModel):
    uploaded_by:UUID
    task_id:UUID
    comment_id:UUID
    file_name:str=Field(...,min_length=4,max_length=255,description='file name')
    file_url:str
    file_type:str=Field(...,max_digits=20,description='type of a file that attached')

class UpdateAttachment(BaseModel):
    file_name:Optional[str]=Field(None,min_length=4,max_length=255,description='file name')
    file_url:Optional[str]=None
    file_type:Optional[str]=Field(None,max_digits=20,description='type of a file that attached')

class AttachmentResponse(CreateAttachment):
    created_at:datetime=Field(...,description='attachment created time')
