from fastapi import APIRouter,status,Depends
from core.database import get_db
from projects.schemas import (ProjectResponse,CreateProject,CreatedResponse,MessageResponse,UpdateProject,ProjectMemberResponse,AddProjectMember,WorkResponse)
from auth.dependencies import get_current_user
from projects.services import (create_project,get_all_projects,delete_project,updateproject,get_project_by_status,get_project_by_name,add_project_member,get_project_members,get_projectmember_byrole,work_details)
from uuid import UUID

project_router=APIRouter(prefix='/projects',tags=['Project Routes'])


#project creating route
@project_router.post('/createproject',response_model=MessageResponse,status_code=status.HTTP_201_CREATED)
async def insert_project(project_details:CreateProject,payload=Depends(get_current_user),db=Depends(get_db)):
    return await create_project(project_details,payload,db)

#get all projects route
@project_router.get('/getprojects',response_model=list[ProjectResponse]|MessageResponse,status_code=status.HTTP_200_OK)
async def get_allprojects(payload=Depends(get_current_user),db=Depends(get_db)):
    return await get_all_projects(payload,db)


#delete project route
@project_router.delete('/deleteproject/{project_id}',response_model=MessageResponse,status_code=status.HTTP_200_OK)
async def delete_Project(project_id:UUID,payload=Depends(get_current_user),db=Depends(get_db)):
    return await delete_project(project_id,payload,db)

@project_router.put('/updateproject/{project_id}',response_model=MessageResponse,status_code=status.HTTP_200_OK)
async def UpdateProject(project_id:UUID,update_details:UpdateProject,payload=Depends(get_current_user),db=Depends(get_db)):
    return await updateproject(project_id,update_details,payload,db)

@project_router.get('/getproject/{status}',response_model=list[ProjectResponse],status_code=status.HTTP_200_OK)
async def get_project(status:str,payload=Depends(get_current_user),db=Depends(get_db)):
    return await get_project_by_status(status,payload,db)

@project_router.get('/getproject/name/{project_name}',response_model=ProjectResponse,status_code=status.HTTP_200_OK)
async def get_project_byname(project_name:str,payload=Depends(get_current_user),db=Depends(get_db)):
    return await get_project_by_name(project_name,payload,db)

@project_router.post('/add/projectmember',response_model=ProjectMemberResponse,status_code=status.HTTP_201_CREATED)
async def create_project_member(member_details:AddProjectMember,payload=Depends(get_current_user),db=Depends(get_db)):
    return await add_project_member(member_details,payload,db)

@project_router.get('/getprojectmember/{project_id}',response_model=list[ProjectMemberResponse]|MessageResponse,status_code=status.HTTP_200_OK)
async def get_all_project_members(project_id:UUID,payload=Depends(get_current_user),db=Depends(get_db)):
    return await get_project_members(project_id,payload,db)

@project_router.get('/get/projectmember/role/{role}',response_model=list[ProjectMemberResponse]|MessageResponse,status_code=status.HTTP_200_OK)
async def get_member_byrole(role:str,payload=Depends(get_current_user),db=Depends(get_db)):
    return await get_projectmember_byrole(role,payload,db)

@project_router.get('/get/work/details',response_model=WorkResponse,status_code=status.HTTP_200_OK)
async def work_progress(payload=Depends(get_current_user),db=Depends(get_db)):
    return await work_details(payload,db)