from fastapi import APIRouter
from epics.schemas import EpicResponse,CreateEpic,UpdateEpic,MessageResponse,TaskResponse,CreateTask,UpdateTask,AssignTaskUser,UserstoryResponse,CreateStory,UpdateStory,TaskDependsResponse,AddTaskDependency,Delete_depends
from fastapi import status,Depends
from auth.dependencies import get_current_user
from core.database import get_db
from epics.services import create_epic,update_epic,delete_epic,getall_epics,searchby_epic_id,create_task,update_task,display_task,display_task_by_assigny,assign_task,delete_task,search_task
from epics.services import create_userstory,getall_userstories,update_userstory,delete_userstory,get_userstory_by_search,add_task_depend,getall_taskdepends,delete_taskdepends,display_task_sprint

epic_router=APIRouter(prefix='/epics',tags=['Epic Route'])

@epic_router.post('/create/epic',response_model=MessageResponse,status_code=status.HTTP_201_CREATED)
async def add_epic(epic_details:CreateEpic,payload=Depends(get_current_user),db=Depends(get_db)):
    return await create_epic(epic_details,payload,db)

@epic_router.put('/update/epic/{epic_id}',response_model=EpicResponse|MessageResponse,status_code=status.HTTP_200_OK)
async def update_epic_byid(epic_id:str,epic_details:UpdateEpic,payload=Depends(get_current_user),db=Depends(get_db)):
    return await update_epic(epic_id,epic_details,payload,db)

@epic_router.delete('/delete/epic/{epic_id}',response_model=MessageResponse,status_code=status.HTTP_200_OK)
async def delete_epic_byid(epic_id:str,payload=Depends(get_current_user),db=Depends(get_db)):
    return await delete_epic(epic_id,payload,db)

@epic_router.get('/getepics/{project_id}',response_model=list[EpicResponse]|MessageResponse,status_code=status.HTTP_200_OK)
async def get_epics(project_id:str,payload=Depends(get_current_user),db=Depends(get_db)):
    return await getall_epics(project_id,payload,db)

@epic_router.get('/getepics/title/{epic_title}',response_model=EpicResponse|MessageResponse,status_code=status.HTTP_200_OK)
async def searchby_epicid(epic_title:str,payload=Depends(get_current_user),db=Depends(get_db)):
    return await searchby_epic_id(epic_title,payload,db)

@epic_router.post('/create/task',response_model=TaskResponse|MessageResponse,status_code=status.HTTP_201_CREATED)
async def add_task(task_details:CreateTask,payload=Depends(get_current_user),db=Depends(get_db)):
    return await create_task(task_details,payload,db)

@epic_router.put('/task/update/{task_id}',response_model=TaskResponse|MessageResponse,status_code=status.HTTP_200_OK)
async def update_task_byid(task_id:str,task_details:UpdateTask,payload=Depends(get_current_user),db=Depends(get_db)):
    return await update_task(task_id,task_details,payload,db)

#searching tasks with project_id or userstory_id
@epic_router.get('/get/task/{search_id}',response_model=list[TaskResponse]|MessageResponse,status_code=status.HTTP_200_OK)
async def displaytask(search_id:str,payload=Depends(get_current_user),db=Depends(get_db)):
    return await display_task(search_id,payload,db)

@epic_router.get('/get/task/title/{title}',response_model=TaskResponse|MessageResponse,status_code=status.HTTP_200_OK)
async def gettask_bytitle(title:str,payload=Depends(get_current_user),db=Depends(get_db)):
    return await search_task(title,payload,db)

@epic_router.get('/get/tasks',response_model=list[TaskResponse]|MessageResponse,status_code=status.HTTP_200_OK)
async def get_tasks_by_assign(payload=Depends(get_current_user),db=Depends(get_db)):
    return await display_task_by_assigny(payload,db)

@epic_router.get('/get/tasks/{sprint_id}',response_model=list[TaskResponse]|MessageResponse,status_code=status.HTTP_200_OK)
async def get_task_sprint(sprint_id,payload=Depends(get_current_user),db=Depends(get_db)):
    return await display_task_sprint(sprint_id,payload,db)

@epic_router.delete('/task/delete/{task_id}',response_model=MessageResponse,status_code=status.HTTP_200_OK)
async def deletetask_byid(task_id:str,payload=Depends(get_current_user),db=Depends(get_db)):
    return delete_task(task_id,payload,db)

@epic_router.get('/add/task/assign',response_model=MessageResponse,status_code=status.HTTP_200_OK)
async def add_assign_task(assign_details:AssignTaskUser,payload=Depends(get_current_user),db=Depends(get_db)):
    return await assign_task(assign_details,payload,db)

@epic_router.post('/create/userstory',response_model=UserstoryResponse,status_code=status.HTTP_201_CREATED)
async def add_user_story(story_details:CreateStory,payload=Depends(get_current_user),db=Depends(get_db)):
    return await create_userstory(story_details,payload,db)

@epic_router.put('/update/userstory/{story_id}',response_model=UserstoryResponse|MessageResponse,status_code=status.HTTP_200_OK)
async def update_user_story(story_id:str,story_details:UpdateStory,payload=Depends(get_current_user),db=Depends(get_db)):
    return await update_userstory(story_id,story_details,payload,db)

@epic_router.delete('/delete/userstory/{story_id}',response_model=MessageResponse,status_code=status.HTTP_200_OK)
async def delete_user_story(story_id:str,payload=Depends(get_current_user),db=Depends(get_db)):
    return await delete_userstory(story_id,payload,db)

@epic_router.get('/get/userstories/{epic_id}',response_model=list[UserstoryResponse]|MessageResponse,status_code=status.HTTP_200_OK)
async def display_userstories(epic_id:str,payload=Depends(get_current_user),db=Depends(get_db)):
    return await getall_userstories(epic_id,payload,db)

@epic_router.get('/get/userstory/{search_id}',response_model=UserstoryResponse|MessageResponse,status_code=status.HTTP_200_OK)
async def display_userstory(search_id:str,payload=Depends(get_current_user),db=Depends(get_db)):
    return await get_userstory_by_search(search_id,payload,db)

@epic_router.post('/taskdepends/create',response_model=TaskDependsResponse,status_code=status.HTTP_201_CREATED)
async def create_task_depends(depends_details:AddTaskDependency,payload=Depends(get_current_user),db=Depends(get_db)):
    return await add_task_depend(depends_details,payload,db)

@epic_router.get('/get/taskdepends/{task_id}',response_model=list[TaskDependsResponse],status_code=status.HTTP_200_OK)
async def display_task_depends(task_id:str,payload=Depends(get_current_user),db=Depends(get_db)):
    return await getall_taskdepends(task_id,payload,db)

@epic_router.delete('/delete/taskdepends',response_model=MessageResponse,status_code=status.HTTP_200_OK)
async def drop_taskdepends(task:Delete_depends,payload=Depends(get_current_user),db=Depends(get_db)):
    return await delete_taskdepends(task,payload,db)