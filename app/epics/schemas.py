from pydantic import Field,BaseModel
from datetime import date,datetime
from typing import Optional
from uuid import UUID

#epic response model 
class EpicResponse(BaseModel):
    id:UUID
    project_id:UUID
    title:str
    description:str
    status:str
    priority:str
    created_by:str
    created_at:datetime
    updated_at:datetime

#create epics model
class CreateEpic(BaseModel):
    project_id:UUID=Field(...,description='unique id of project that epic is created')
    title:str=Field(...,min_length=4,max_length=225,description='title of the epic')
    description:str=Field(...,min_length=8,description='description of the epic')
    status:str=Field(...,min_length=4,max_length=20,description='current satate of the epic')
    priority:str=Field(...,min_length=4,max_length=20,description='priority of the project stays here')

class UpdateEpic(BaseModel):
    title:Optional[str]=Field(None,min_length=3,max_length=225,description='title of the epic')
    description:Optional[str]=Field(None,min_length=8,description='description of the epic')
    status:Optional[str]=Field(None,min_length=4,max_length=20,description='current state of the epic')
    priority:Optional[str]=Field(None,min_length=4,max_length=20,description='priority of the epic')

#create user story model
class CreateStory(BaseModel):
    epic_id:UUID=Field(...,description='unique id of epic that story created at')
    title:str=Field(...,min_length=3,max_length=225,description='title of the user story')
    description:str=Field(...,min_length=8,description='description of the user story')
    acceptance_criteria:str=Field(...,min_length=8,description='explains the bugs or the features to update with detail solution')
    priority:str=Field(...,min_length=3,max_length=20,description='priority of user story')
    story_points:int=Field(...,lt=6,gt=0,description='story points can be added between 1 to 5')
    status:str=Field(...,min_length=4,max_length=20,description='current satate of the epic')

class UpdateStory(BaseModel):
    title:Optional[str]=Field(None,min_length=4,max_length=225,description='title of the user story')
    description:Optional[str]=Field(None,min_length=8,description='description of the user story')
    acceptance_criteria:Optional[str]=Field(None,min_length=8,description='acceptance criteria for the user story')
    priority:Optional[str]=Field(None,min_length=4,max_length=20,description='priority of user story')
    story_points:Optional[int]=Field(None,lt=6,gt=0,description='story points can be added between 1 to 5')
    status:Optional[str]=Field(None,min_length=4,max_length=20,description='current state of the user story')

#user story response model
class UserstoryResponse(BaseModel):
    id:UUID
    epic_id:UUID
    title:str
    description:str
    acceptance_criteria:str
    priority:str
    story_points:int
    status:str
    created_by:UUID
    created_at:datetime
    updated_at:datetime

#create task model
class CreateTask(BaseModel):
    project_id:UUID=Field(...,description='unique id of project')
    user_story_id:UUID=Field(...,description='unique id of user story')
    title:str=Field(...,min_length=3,max_length=225,description='title of the user story')
    description:str=Field(...,min_length=8,description='description of the user story')
    priority:str=Field(...,min_length=3,max_length=20,description='priority of task')
    status:str=Field(...,min_length=3,max_length=20,description='current satate of the task')
    assigned_to:Optional[UUID]=Field(None,description='user id that task is assigned to')
    estimated_hours:float=Field(...,description='estimated time to complete this task')
    actual_hours:float=Field(...,description='actual time to complete the task in hours')
    due_date:date=Field(...,description='due date of task')

class UpdateTask(BaseModel):
    title:Optional[str]=Field(None,min_length=4,max_length=225,description='title of the task')
    description:Optional[str]=Field(None,min_length=8,description='description of the task')
    priority:Optional[str]=Field(None,min_length=4,max_length=20,description='priority of task')
    status:Optional[str]=Field(None,min_length=4,max_length=20,description='current state of the task')
    assigned_to:Optional[UUID]=Field(None,description='user id that task is assigned to')
    estimated_hours:Optional[float]=Field(None,description='estimated time to complete this task')
    actual_hours:Optional[float]=Field(None,description='actual time to complete the task in hours')
    due_date:Optional[date]=Field(None,description='due date of task')
    completed_at:Optional[date]=Field(None,description='completed date of task')

#task response model
class TaskResponse(BaseModel):
    id:UUID
    project_id:UUID
    user_story_id:UUID
    title:str
    description:str
    priority:str
    status:str
    assigned_to:Optional[str]
    created_by:UUID|str
    estimated_hours:float
    actual_hours:float
    due_date:date
    created_at:datetime
    updated_at:datetime
    completed_at:Optional[datetime]

class AssignTaskUser(BaseModel):
    task_id:UUID=Field(...,description='unique id of a task')
    user_id:UUID=Field(...,description='unique id of a user for whom the task wanted to assign')

class AddTaskDependency(BaseModel):
    task_id:UUID=Field(...,description='unique task id')
    depends_on_task_id:UUID=Field(...,description='unique task id which depends on current task')
    dependency_type:str=Field(...,description='type of dependency')

class TaskDependsResponse(BaseModel):
    id:UUID
    task_id:UUID
    depends_on_task_id:UUID
    created_at:datetime

class Delete_depends(BaseModel):
    task_id:UUID=Field(...,description='unique task id')
    depends_on_task_id:UUID=Field(...,description='unique task id which depends on current task')

class MessageResponse(BaseModel):
    message:str