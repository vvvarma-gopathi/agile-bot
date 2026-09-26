from pydantic import Field,BaseModel
from datetime import date,datetime
from typing import Optional
from uuid import UUID


class CreateProject(BaseModel):
    name:str=Field(...,max_length=225,min_length=7,description='name of projects')
    description:str=Field(...,min_length=20,description='description of project')
    goal:str=Field(...,min_length=20,description='goal of project')
    status:str=Field(...,min_length=4,max_length=20,description='status of the project(active/completed/inactive)')
    start_date:date=Field(...,description='project end date')
    end_date:date=Field(...,description='project end date')

#project response model used when project created
class CreatedResponse(CreateProject):
    name:str=Field(...,max_length=225,min_length=7,description='name of projects')
    description:str=Field(...,min_length=20,description='description of project')
    goal:str=Field(...,min_length=20,description='goal of project')
    status:str=Field(...,min_length=4,max_length=20,description='status of the project(active/completed/inactive)')
    end_date:date=Field(...,description='project end date')
    start_date:date=Field(...,description='project end date')
    owner_id:str=Field(...,max_length=225,min_length=20,description='unique id of projects')
    owner:str=Field(...,min_length=4,max_length=100,description='user name of user who created project')

class ProjectResponse(CreateProject):
    id:UUID=Field(...,description='unique id of projects')
    created_by:str=Field(...,min_length=3,max_length=225,description='owner name')
    owner_id:UUID
    name:str=Field(...,max_length=225,min_length=7,description='name of projects')
    description:str=Field(...,min_length=20,description='description of project')
    goal:str=Field(...,min_length=20,description='goal of project')
    status:str=Field(...,min_length=4,max_length=20,description='status of the project(active/completed/inactive)')
    start_date:date=Field(...,description='project start date')
    end_date:date=Field(...,description='project end date')
    updated_at:datetime=Field(...,description='project update time')
    created_at:datetime=Field(...,description='project created date')
    total_sprints:Optional[int]
    total_epics:Optional[int]
    total_tasks:Optional[int]
    completed_tasks:Optional[int]



class UpdateProject(BaseModel):
    owner_id:Optional[UUID]=Field(default=None)
    name:Optional[str]=Field(default=None,max_length=225,min_length=7,description='name of projects')
    description:Optional[str]=Field(default=None,min_length=20,description='description of project')
    goal:Optional[str]=Field(default=None,min_length=20,description='goal of project')
    status:Optional[str]=Field(default=None,min_length=4,max_length=20,description='status of the project(active/completed/inactive)')
    end_date:Optional[date]=Field(default=None,description='project end date')

class AddProjectMember(BaseModel):
    project_id:UUID=Field(...,description='unique project id')
    user_id:UUID=Field(...,description='unique user id of role developers')
    project_role:str=Field(...,min_length=5,max_length=225,description='unique project id')

class ProjectMemberResponse(BaseModel):
    id:UUID
    project_id:UUID
    user_id:UUID
    user_name:Optional[str]
    project_role:str
    joined_at:datetime
    is_active:bool

class MessageResponse(BaseModel):
    message:str

class WorkResponse(BaseModel):
    total_projects:int
    total_tasks:int
    total_sprints:int
    total_epics:int