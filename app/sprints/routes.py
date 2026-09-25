from uuid import UUID

from fastapi import APIRouter, Depends, status

from auth.dependencies import get_current_user
from core.database import get_db
from sprints.schemas import (
	CreateSprint,
	CreateSprintItems,
	MessageResponse,
	SprintItemResponse,
	SprintResponse,
	UpdateSprint,
	UpdateSprintItems,
)
from sprints.services import (
	create_sprint,
	create_sprint_item,
	delete_sprint,
	delete_sprint_item,
	update_sprint,
	update_sprint_item,
	get_sprints_by_id,
	get_sprintitems,
	get_allsprints,
	get_all_sprintitems
)


sprint_router = APIRouter(prefix='/sprints', tags=['Sprint Routes'])


@sprint_router.post('/create', response_model=SprintResponse, status_code=status.HTTP_201_CREATED)
async def create_sprint_route(
	sprint_details: CreateSprint,
	payload=Depends(get_current_user),
	db=Depends(get_db),
):
	return await create_sprint(sprint_details, payload, db)


@sprint_router.put('/update/{sprint_id}', response_model=SprintResponse, status_code=status.HTTP_200_OK)
async def update_sprint_route(
	sprint_id: UUID,
	sprint_details: UpdateSprint,
	payload=Depends(get_current_user),
	db=Depends(get_db),
):
	return await update_sprint(sprint_id, sprint_details, payload, db)


@sprint_router.delete('/delete/{sprint_id}', response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def delete_sprint_route(
	sprint_id: UUID,
	payload=Depends(get_current_user),
	db=Depends(get_db),
):
	return await delete_sprint(sprint_id, payload, db)


@sprint_router.post('/items/create', response_model=SprintItemResponse, status_code=status.HTTP_201_CREATED)
async def create_sprint_item_route(
	item_details: CreateSprintItems,
	payload=Depends(get_current_user),
	db=Depends(get_db),
):
	return await create_sprint_item(item_details, payload, db)


@sprint_router.put('/items/update/{item_id}', response_model=SprintItemResponse, status_code=status.HTTP_200_OK)
async def update_sprint_item_route(
	item_id: UUID,
	item_details: UpdateSprintItems,
	payload=Depends(get_current_user),
	db=Depends(get_db),
):
	return await update_sprint_item(item_id, item_details, payload, db)


@sprint_router.delete('/items/delete/{item_id}', response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def delete_sprint_item_route(
	item_id: UUID,
	payload=Depends(get_current_user),
	db=Depends(get_db),
):
	return await delete_sprint_item(item_id, payload, db)

@sprint_router.get('/get/sprint/{search_id}',response_model=SprintResponse,status_code=status.HTTP_200_OK)
async def get_sprint_details(search_id:str,payload=Depends(get_current_user),db=Depends(get_db)):
	return await get_sprints_by_id(search_id,payload,db)

@sprint_router.get('/get/sprint/item/{search_id}',response_model=SprintItemResponse,status_code=status.HTTP_200_OK)
async def get_sprintitem(search_id:str,payload=Depends(get_current_user),db=Depends(get_db)):
	return await get_sprintitems(search_id,payload,db)

@sprint_router.get('/getall/sprints/{project_id}',response_model=list[SprintResponse]|MessageResponse,status_code=status.HTTP_200_OK)
async def getall_sprints(project_id:str,payload=Depends(get_current_user),db=Depends(get_db)):
	return await get_allsprints(project_id,payload,db)

@sprint_router.get('/getall/sprintitems/{sprint_id}',response_model=list[SprintItemResponse]|MessageResponse,status_code=status.HTTP_200_OK)
async def getall_sprintitems(sprint_id:str,payload=Depends(get_current_user),db=Depends(get_db)):
	return await get_all_sprintitems(sprint_id,payload,db)
