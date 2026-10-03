from app.epics.schemas import CreateEpic,UpdateEpic,MessageResponse,CreateTask,UpdateTask,AssignTaskUser,CreateStory,UpdateStory,AddTaskDependency,Delete_depends,EpicResponse,TaskResponse
from fastapi import HTTPException,status
from app.epics.models import Epics,Tasks,UserStories,TaskDependencies
from uuid import UUID
from app.sprints.models import Sprints,SprintItems
from app.auth.models import Users
from sqlalchemy import delete, select, update

def create_epic_helper(epic:dict)->Epics:
    return Epics(**epic)

def create_task_helper(tasks:dict)->Tasks:
    return Tasks(**tasks)

def create_userstory_helper(userstory:dict)->UserStories:
    return UserStories(**userstory)

async def create_epic(epic_details:CreateEpic,payload,db):
    epic=epic_details.model_dump()
    epic['created_by']=payload['id']
    fetch_epic=db.scalar(select(Epics).where(Epics.title==epic['title'], Epics.project_id==epic['project_id']))
    if fetch_epic:
        return MessageResponse(message=f'epic with title {epic['title']} already exist kindly change the title to create one!')
    epic_record=create_epic_helper(epic)
    db.add(epic_record)
    db.flush()
    db.commit()
    db.refresh(epic_record)
    return MessageResponse(message='epic created successfully..')

async def update_epic(epic_id:str,epic_details:UpdateEpic,payload,db):
    epic_record=db.scalar(select(Epics).where(Epics.id==epic_id))
    if not epic_record:
        return MessageResponse(message='No epic found to update..')
    updates=epic_details.model_dump(exclude_unset=True,exclude_none=True)
    if not updates:
        return MessageResponse(message='No epic fields provided to update..')
    if 'title' in updates and db.scalar(select(Epics).where(Epics.title==updates['title'],Epics.id!=epic_id)):
        return MessageResponse(message=f'Epic with title "{updates["title"]}" already exists')
    for field,value in updates.items():
        setattr(epic_record,field,value)
    db.commit()
    db.refresh(epic_record)
    return MessageResponse(message='epic updated successfully.')

async def delete_epic(epic_id:str,payload,db):
    epic_record=db.scalar(select(Epics).where(Epics.id==epic_id))
    if not epic_record:
        return MessageResponse(message='No epic found to delete..')
    db.delete(epic_record)
    db.commit()
    return MessageResponse(message=f'Epic deleted successfully with id {epic_id}')

async def getall_epics(project_id:str,payload,db):
    results=[]
    epic_records=db.scalars(select(Epics).where(Epics.project_id==project_id)).all()
    if not epic_records:
        return MessageResponse(message=f'no records found with project_id {project_id}')
    for record in epic_records:
        created_by=db.execute(select(Users.user_name).where(Users.id==record.created_by)).scalar()
        results.append(EpicResponse(id=record.id,project_id=record.project_id,title=record.title,description=record.description,status=record.status,created_by=created_by,priority=record.priority,created_at=record.created_at,updated_at=record.updated_at))
    return results

async def searchby_epic_id(epic_title:str,payload,db):
    epic_record=db.scalar(select(Epics).where(Epics.title==epic_title.replace('+',' ')))
    if not epic_record:
        return MessageResponse(message=f'No epics found with title "{epic_title}".')
    return epic_record

async def create_task(task_details:CreateTask,payload,db):
    if db.scalar(select(Tasks).where(Tasks.title==task_details.title)):
        return MessageResponse(message=f'Task with title "{task_details.title}" already exists in tasks change the title to insert another task')
    task_data=task_details.model_dump()
    task_data['created_by']=payload['id']
    task_record=create_task_helper(task_data)
    db.add(task_record)
    db.flush()
    db.commit()
    db.refresh(task_record)
    return task_record

async def update_task(task_id:str,task_details:UpdateTask,payload,db):
    task_record=db.scalar(select(Tasks).where(Tasks.id==task_id))
    if not task_record:
        return MessageResponse(message='No Task found to update..')
    updates=task_details.model_dump(exclude_unset=True)
    if not updates:
        return MessageResponse(message='No task fields provided to update..')
    if 'status' in updates and len(updates)==1:
            if payload['role_id'] in (1,3) or task_record.assigned_to:
                if payload['id']!=task_record.assigned_to and payload['role_id'] not in (1,3):
                    return MessageResponse(message='only a assigny can change task state')
                for field,value in updates.items():
                    setattr(task_record,field,value)
                db.commit()
                db.refresh(task_record)
                return MessageResponse(message='updated task state successfully')
            else:
                return MessageResponse(message='only a assigny can change task state')
    else:
        if payload['role_id']!=1 and payload['role_id']!=3:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='only a project manager or admin can update tasks..')
        if 'title' in updates and db.scalar(select(Tasks).where(Tasks.title==updates['title'],Tasks.id!=task_id)):
            return MessageResponse(message=f'Task with title "{updates["title"]}" already exists in tasks')
        for field,value in updates.items():
            setattr(task_record,field,value)
        db.commit()
        db.refresh(task_record)
        return MessageResponse(message='updated successfully..')

async def display_task(search_id:str,payload,db):
    task_records=db.scalars(select(Tasks).where(Tasks.user_story_id==search_id)).all()
    if not task_records:
        return MessageResponse(message='No tasks found create one!')
    return task_records

async def search_task(title:str,payload,db):
    task_record=db.scalar(select(Tasks).where(Tasks.title==title))
    if not task_record:
        return MessageResponse(message='No tasks found create one!')
    return task_record

async def display_task_by_assigny(payload,db):
    task_records=db.scalars(select(Tasks).where(Tasks.assigned_to==payload['id'])).all()
    if not task_records:
        return MessageResponse(message='No tasks assigned to you..')
    return task_records

async def display_task_sprint(sprint_id,payload,db):
    results=[]
    query=(select(SprintItems.task_id).join(Sprints,Sprints.id==SprintItems.sprint_id).where(Sprints.id==sprint_id))
    tasks_ids=db.execute(query).scalars().all()
    if not tasks_ids:
        return MessageResponse(message='No sprints found!')
    tasks=db.scalars(select(Tasks).where(Tasks.id.in_(tasks_ids))).all()
    if not tasks:
        return MessageResponse(message='No sprints found!')
    for record in tasks:
        assigned_name='not assigned'
        if record.assigned_to:
            assigned_name=db.scalar(select(Users.user_name).where(Users.id==record.assigned_to))
        print(record.created_by)
        user=db.scalar(select(Users).where(Users.id==record.created_by))
        print(user.user_name)
        results.append(TaskResponse(id=record.id,project_id=record.project_id,user_story_id=record.user_story_id,
                                    title=record.title,description=record.description,priority=record.priority,
                                    status=record.status,assigned_to=assigned_name,created_by=user.user_name,estimated_hours=record.estimated_hours
                                    ,actual_hours=record.actual_hours,created_at=record.created_at,updated_at=record.updated_at,
                                    completed_at=record.completed_at,due_date=record.due_date,))
    return results

async def assign_task(assign_details:AssignTaskUser,payload,db):
    if db.scalar(select(Tasks).where(Tasks.id==assign_details.task_id, Tasks.assigned_to==assign_details.user_id)):
        return MessageResponse(message='Task already assigned to user..')
    db.execute(update(Tasks).where(Tasks.id==assign_details.task_id).values(assigned_to=assign_details.user_id).execution_options(synchronize_session='fetch'))
    db.commit()
    return MessageResponse(message='Task successfully assigned..')

async def delete_task(task_id:str,payload,db):
    if not db.scalar(select(Tasks).where(Tasks.id==task_id)):
        return MessageResponse(message='No Task found to delete..')
    db.execute(delete(Tasks).where(Tasks.id==task_id).execution_options(synchronize_session='fetch'))
    db.commit()
    return MessageResponse(message=f'Task deleted successfully with id {task_id}')

async def create_userstory(story_details:CreateStory,payload,db):
    if db.scalar(select(UserStories).where(UserStories.title==story_details.title)):
        raise HTTPException(status_code=status.HTTP_302_FOUND,detail=f'user story with title "{story_details.title}" already exist.')
    user_stories=story_details.model_dump()
    user_stories['created_by']=payload['id']
    story_record=create_userstory_helper(user_stories)
    db.add(story_record)
    db.flush()
    db.commit()
    db.refresh(story_record)
    return story_record

async def getall_userstories(epic_id:str,payload,db):
    story_records=db.scalars(select(UserStories).where(UserStories.epic_id==epic_id)).all()
    if not story_records:
        return MessageResponse(message=f'No records found with the epic_id "{epic_id}"')
    return story_records

async def update_userstory(story_id:str,story_details:UpdateStory,payload,db):
    story_record=db.scalar(select(UserStories).where(UserStories.id==story_id))
    if not story_record:
        return MessageResponse(message='No user story found to update..')
    updates=story_details.model_dump(exclude_unset=True,exclude_none=True)
    if not updates:
        return MessageResponse(message='No user story fields provided to update..')
    if 'title' in updates and db.scalar(select(UserStories).where(UserStories.title==updates['title'],UserStories.id!=story_id)):
        return MessageResponse(message=f'User story with title "{updates["title"]}" already exists')
    for field,value in updates.items():
        setattr(story_record,field,value)
    db.commit()
    db.refresh(story_record)
    return story_record

async def delete_userstory(story_id:str,payload,db):
    story_record=db.scalar(select(UserStories).where(UserStories.id==story_id))
    if not story_record:
        return MessageResponse(message='No user story found to delete..')
    db.delete(story_record)
    db.commit()
    return MessageResponse(message=f'User story deleted successfully with id {story_id}')

async def get_userstory_by_search(search_id,payload,db):
    search_value=search_id.replace('+',' ')
    story_record=db.scalar(select(UserStories).where(UserStories.title==search_value))
    if not story_record:
        try:
            story_record=db.scalar(select(UserStories).where(UserStories.id==UUID(search_id)))
        except ValueError:
            story_record=None
    if not story_record:
        return MessageResponse(message='No user story is found.')
    return story_record

#adding task dependencies for tasks
async def add_task_depend(depend_details:AddTaskDependency,payload,db):
    task=db.scalar(select(Tasks).where(Tasks.id==depend_details.task_id))
    if not task:
        return MessageResponse(message='No task fount to add dependencies')
    dependency_record=TaskDependencies(**depend_details.model_dump())
    db.add(dependency_record)
    db.commit()
    db.refresh(dependency_record)
    return dependency_record

async def getall_taskdepends(task_id:str,payload,db):
    taskdepends_records=db.scalars(select(TaskDependencies).where(TaskDependencies.task_id==task_id)).all()
    if not taskdepends_records:
        return MessageResponse(message='No dependencies found')
    return taskdepends_records

async def delete_taskdepends(task:Delete_depends,payload,db):
    task_record=db.scalar(select(TaskDependencies).where(TaskDependencies.task_id==task.task_id, TaskDependencies.depends_on_task_id==task.depends_on_task_id))
    if not task_record:
        return MessageResponse(message='No task dependencies to delete')
    db.delete(task_record)
    db.commit()
    return MessageResponse(message='Task depency deleted successfully')

    
    