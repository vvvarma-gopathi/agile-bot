from uuid import UUID, uuid4

from fastapi import HTTPException, status
from auth.dependencies import validate_user
from projects.models import Projects
from epics.models import Tasks
from sprints.models import SprintItems, Sprints
from sprints.schemas import (
	CreateSprint,
	CreateSprintItems,
	MessageResponse,
	UpdateSprint,
	UpdateSprintItems,
)

#checking permission for project manager and admin roles
def _require_project_manager(payload, project_id: UUID, db):
	if payload['role_id'] not in (1, 3):
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail='Only an admin or project manager can manage sprints',
		)

	project = db.query(Projects).filter(Projects.id == project_id).first()
	if not project:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f'No project exists with id={project_id}',
		)

	if payload['role_id'] == 3 and project.owner_id != UUID(payload['id']):
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail='You can only manage sprints in your own projects',
		)

	return project

#get sprint function 
async def _get_sprint(id,db):
	sprint=db.query(Sprints).filter(Sprints.id==id).first()
	if not sprint:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='no sprints found')
	return sprint

#creating sprint by checking role wise features
async def create_sprint(sprint_details: CreateSprint, payload, db):
	_require_project_manager(payload, sprint_details.project_id, db)

	existing_sprint = db.query(Sprints).filter(Sprints.name == sprint_details.name).first()
	if existing_sprint:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail='A sprint with this name already exists',
		)

	sprint = Sprints(
		**sprint_details.model_dump(),
		created_by=UUID(payload['id']),
	)
	db.add(sprint)
	db.commit()
	db.refresh(sprint)
	return MessageResponse(message='sprint successfully created...')

#get sprint by id
async def get_sprints_by_id(search_id,payload,db):
	if not payload['id']:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='invalid user credentials please login.')
	sprint_by_title=db.query(Sprints).filter(Sprints.title==search_id.replace('+',' ')).first()
	if not sprint_by_title:
		return _get_sprint(UUID(search_id),db)

#update sprint function
async def update_sprint(sprint_id: UUID, sprint_details: UpdateSprint, payload, db):
	sprint = db.query(Sprints).filter(Sprints.id == sprint_id).first()
	if not sprint:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f'No sprint exists with id={sprint_id}',
		)

	_require_project_manager(payload, sprint.project_id, db)

	update_data = sprint_details.model_dump(exclude_unset=True)
	start_date = update_data.get('start_date', sprint.start_date)
	end_date = update_data.get('end_date', sprint.end_date)
	if end_date <= start_date:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail='end_date must be after start_date',
		)

	if 'name' in update_data:
		duplicate = db.query(Sprints).filter(
			Sprints.name == update_data['name'],
			Sprints.id != sprint_id,
		).first()
		if duplicate:
			raise HTTPException(
				status_code=status.HTTP_409_CONFLICT,
				detail='A sprint with this name already exists',
			)

	for field, value in update_data.items():
		setattr(sprint, field, value)
	db.commit()
	db.refresh(sprint)
	return MessageResponse(message='Sprint updated successfully..')

#delete sprint function
async def delete_sprint(sprint_id: UUID, payload, db):
	sprint = db.query(Sprints).filter(Sprints.id == sprint_id).first()
	if not sprint:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f'No sprint exists with id={sprint_id}',
		)

	_require_project_manager(payload, sprint.project_id, db)
	db.delete(sprint)
	db.commit()
	return MessageResponse(message='Sprint deleted successfully')


def _get_sprint_item(item_id: UUID, db):
	item = db.query(SprintItems).filter(SprintItems.id == item_id).first()
	if not item:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f'No sprint item exists with id={item_id}',
		)
	return item


def _validate_task_for_sprint(task_id: UUID, sprint, db):
	task = db.query(Tasks).filter(Tasks.id == task_id).first()
	if not task:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f'No task exists with id={task_id}',
		)
	if task.project_id != sprint.project_id:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail='The task must belong to the sprint project',
		)


async def create_sprint_item(item_details: CreateSprintItems, payload, db):
	sprint = db.query(Sprints).filter(Sprints.id == item_details.sprint_id).first()
	if not sprint:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f'No sprint exists with id={item_details.sprint_id}',
		)

	_require_project_manager(payload, sprint.project_id, db)
	_validate_task_for_sprint(item_details.task_id, sprint, db)

	existing_item = db.query(SprintItems).filter(
		SprintItems.sprint_id == item_details.sprint_id,
		SprintItems.task_id == item_details.task_id,
	).first()
	if existing_item:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail='This task is already assigned to the sprint',
		)

	item = SprintItems(
		id=uuid4(),
		sprint_id=item_details.sprint_id,
		task_id=item_details.task_id,
	)
	db.add(item)
	db.commit()
	db.refresh(item)
	return item


async def update_sprint_item(item_id: UUID, item_details: UpdateSprintItems, payload, db):
	item = _get_sprint_item(item_id, db)
	current_sprint = db.query(Sprints).filter(Sprints.id == item.sprint_id).first()
	_require_project_manager(payload, current_sprint.project_id, db)

	update_data = item_details.model_dump(exclude_unset=True)
	if not update_data:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail='At least one sprint item field must be provided',
		)

	target_sprint = current_sprint
	if 'sprint_id' in update_data:
		target_sprint = db.query(Sprints).filter(Sprints.id == update_data['sprint_id']).first()
		if not target_sprint:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail=f"No sprint exists with id={update_data['sprint_id']}",
			)
		_require_project_manager(payload, target_sprint.project_id, db)

	target_task_id = update_data.get('task_id', item.task_id)
	_validate_task_for_sprint(target_task_id, target_sprint, db)

	duplicate = db.query(SprintItems).filter(
		SprintItems.sprint_id == target_sprint.id,
		SprintItems.task_id == target_task_id,
		SprintItems.id != item_id,
	).first()
	if duplicate:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail='This task is already assigned to the sprint',
		)

	for field, value in update_data.items():
		setattr(item, field, value)
	db.commit()
	db.refresh(item)
	return item


async def delete_sprint_item(item_id: UUID, payload, db):
	item = _get_sprint_item(item_id, db)
	sprint = db.query(Sprints).filter(Sprints.id == item.sprint_id).first()
	_require_project_manager(payload, sprint.project_id, db)
	db.delete(item)
	db.commit()
	return MessageResponse(message='Sprint item deleted successfully')

async def get_sprintitems(search_id,payload,db):
	if not payload['id']:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='invalid user credentials, please login!')
	sprint_item=db.query(SprintItems).filter(SprintItems.title==search_id.replace('+',' ')).first()
	if not sprint_item:
		return _get_sprint_item(UUID(search_id),db)

#get all sprints and sprints item functions starts from here.....

async def get_allsprints(project_id,payload,db):
	validate_user(payload)
	sprints=db.query(Sprints).filter(Sprints.project_id==project_id).all()
	if not sprints:
		return MessageResponse(message='No sprints found')
	return sprints

async def get_all_sprintitems(sprint_id,payload,db):
	validate_user(payload)
	sprint=db.query(Sprints).filter(Sprints.id==sprint_id).first()
	if not sprint:
		return MessageResponse(message='Invalid sprint, no sprint found')
	sprint_items=db.query(SprintItems).filter(SprintItems.sprint_id==sprint_id).all()
	if not sprint_items:
		return MessageResponse(message='No items in the sprint')
	return sprint_items