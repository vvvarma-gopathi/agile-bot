from projects.schemas import CreateProject,UpdateProject,MessageResponse,AddProjectMember,WorkResponse,ProjectResponse
from auth.dependencies import get_current_user,validate_user
from projects.models import Projects,Project_members
from fastapi import HTTPException,status
from uuid import UUID
from sqlalchemy import select,func
from epics.models import Tasks,Epics
from sprints.models import Sprints
from auth.models import Users


def work_details_helper(work_details:dict)->WorkResponse:
    return WorkResponse(**work_details)

#helper function for create function to add project manager himself as a project member
def helper_add_project_member(details:dict)->Project_members:
    return Project_members(
        user_id=details['user_id'],
        project_id=details['project_id'],
        project_role=details['role']
        )

#helper function for creating project
def helper_function(project_record:dict):
    return Projects(**project_record)

#helper function for adding project members
def add_member_helper(details:dict)->Project_members:
    return Project_members(**details)

#Creating the project only by the current logedin user and role is project manager
async def create_project(project_details:CreateProject,payload,db):
    if payload['role_id']==1 or payload['role_id']==3:
        project_data = project_details.model_dump()
        project_data['owner_id']=payload['id']
        project_record = helper_function(project_data)
        db.add(project_record)
        db.flush()
        project_member=helper_add_project_member({"user_id":payload['id'],"project_id":project_record.id,"role":"Project Manager"})
        db.add(project_member)
        db.commit()
        project_data['owner']=payload['user_name']
        return MessageResponse(message='Project created successfully..')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Only a Project Manager can create projects')

#accessing all projects only by the project manager where the projects is owned by him
async def get_all_projects(payload,db):
    if payload['id']:
        records=[]
        p_ids=db.execute(select(Project_members.project_id).where(Project_members.user_id==payload['id'])).scalars().all()
        projects=db.query(Projects).filter(Projects.id.in_(p_ids)).all()
        if not projects:
                    return MessageResponse(message="No projects assosiated with the user create one!")
        for record in projects:
            total_sprints=db.execute(select(func.count(Sprints.id)).where(Sprints.project_id==record.id)).scalar() or 0
            total_tasks=db.execute(select(func.count(Tasks.id)).where(Tasks.project_id==record.id)).scalar() or 0
            completed_tasks=db.execute(select(func.count(Tasks.id)).where(Tasks.project_id==record.id,Tasks.status=='Completed')).scalar() or 0
            total_epics=db.execute(select(func.count(Epics.id)).where(Epics.project_id==record.id)).scalar() or 0
            owner_name=db.execute(select(Users.user_name).where(Users.id==record.owner_id)).scalar()
            print(owner_name)
            records.append(ProjectResponse(id=record.id,created_by=owner_name,name=record.name,description=record.description,goal=record.goal,
                                           status=record.status,start_date=record.start_date,end_date=record.end_date,updated_at=record.updated_at,created_at=record.created_at,
                                            total_tasks=total_tasks,total_sprints=total_sprints,completed_tasks=completed_tasks,total_epics=total_epics))
        return records
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Only a Project Manager can access all projects')

#delete project function project manager and admin are authorized
async def delete_project(project_id:UUID,payload,db):
    if payload['role_id']==1 or payload['role_id']==3:
        record=db.query(Projects).filter(Projects.id==project_id).first()
        print(record)
        if record:
            db.query(Projects).filter(Projects.id==project_id).delete(synchronize_session="fetch")
            db.commit()
            return {"message":"deleted successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='No such project to delete.')


async def updateproject(project_id:UUID,updatedetails:UpdateProject,payload,db):
    if payload['role_id']==1 or payload['role_id']==3:
        record=db.query(Projects).filter(Projects.id==project_id).first()
        if record:
            update_data={k:v for k,v in updatedetails.model_dump().items() if v is not None}
            db.query(Projects).filter(Projects.id==project_id).update(update_data,synchronize_session='fetch')
            db.commit()
            print(update_data)
            return {"message":"Project info updated successfully."}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'No such project exist with id={project_id}')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='only a project manager can update project.')

async def get_project_by_status(status:str,payload,db):
    validate_user(payload)
    records=[]
    id_s = db.execute(select(Project_members.project_id).where(Project_members.user_id==payload['id'])).scalars().all()
    if not id_s:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No projects associated with you..")
    project_details=db.query(Projects).filter(Projects.id.in_(id_s),Projects.status==status).all()
    for record in project_details:
                total_sprints=db.execute(select(func.count(Sprints.id)).where(Sprints.project_id==record.id)).scalar() or 0
                total_tasks=db.execute(select(func.count(Tasks.id)).where(Tasks.project_id==record.id)).scalar() or 0
                completed_tasks=db.execute(select(func.count(Tasks.id)).where(Tasks.project_id==record.id,Tasks.status=='Completed')).scalar() or 0
                total_epics=db.execute(select(func.count(Epics.id)).where(Epics.project_id==record.id)).scalar() or 0
                owner_name=db.execute(select(Users.user_name).where(Users.id==record.owner_id)).scalar()
                records.append(ProjectResponse(id=record.id,created_by=owner_name,name=record.name,description=record.description,goal=record.goal,
                                               status=record.status,start_date=record.start_date,end_date=record.end_date,updated_at=record.updated_at,created_at=record.created_at,
                                                total_tasks=total_tasks,total_sprints=total_sprints,completed_tasks=completed_tasks,total_epics=total_epics))
    return records

async def get_project_by_name(project_name:str,payload,db):
    validate_user(payload)
    project_details=db.query(Projects).filter(Projects.name==project_name).first()
    if not project_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='No project details found')
    auth_details = db.query(Project_members).filter(Project_members.user_id==payload['id'],Project_members.project_id==project_details.id).first()
    if not auth_details:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='only a project member can access the project details')
    total_sprints=db.execute(select(func.count(Sprints.id)).where(Sprints.project_id==project_details.id)).scalar() or 0
    total_tasks=db.execute(select(func.count(Tasks.id)).where(Tasks.project_id==project_details.id)).scalar() or 0
    completed_tasks=db.execute(select(func.count(Tasks.id)).where(Tasks.project_id==project_details.id,Tasks.status=='Completed')).scalar() or 0
    total_epics=db.execute(select(func.count(Epics.id)).where(Epics.project_id==project_details.id)).scalar() or 0
    owner_name=db.execute(select(Users.user_name).where(Users.id==project_details.owner_id)).scalar().one()
    project_details=ProjectResponse(id=project_details.id,created_by=owner_name,name=project_details.name,description=project_details.description,goal=project_details.goal,
                                   status=project_details.status,start_date=project_details.start_date,end_date=project_details.end_date,updated_at=project_details.updated_at,created_at=project_details.created_at,
                                    total_tasks=total_tasks,total_sprints=total_sprints,completed_tasks=completed_tasks,total_epics=total_epics)
    return project_details


async def add_project_member(assign_details:AddProjectMember,payload,db):
    if payload['role_id']!=1 and payload['role_id']!=3:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='only a project manager can add project_members')
    if db.query(Project_members).filter(Project_members.user_id == assign_details.user_id).first():
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,detail='User is already in the project')
    member_record=add_member_helper(assign_details.model_dump())
    db.add(member_record)
    db.flush()
    db.commit()
    return member_record

async def get_project_members(project_id:UUID,payload,db):
    validate_user(payload)
    member_records=db.query(Project_members).filter(Project_members.project_id==project_id).all()
    if not member_records:
       return MessageResponse(message=f'No members assigned for project_id {project_id}')
    return member_records

async def get_projectmember_byrole(role:str,payload,db):
    validate_user(payload)
    project_member_records=db.query(Project_members).filter(Project_members.project_role==role).all()
    if not project_member_records:
        return MessageResponse(message=f'No users found in project with role {role}')
    return project_member_records

async def work_details(payload,db):
    validate_user(payload)
    total_projects=db.execute(select(func.count(Project_members.project_id)).where(Project_members.user_id==payload['id']))
    total_tasks=db.execute(select(func.count(Tasks.id)).where(Tasks.assigned_to==payload['id']))
    total_sprints=db.execute(select(func.count(Sprints.id)).join(Project_members,Sprints.project_id==Project_members.project_id).where(Project_members.user_id==payload['id']))
    total_epics=db.execute(select(func.count(Epics.id)).join(Project_members,Epics.project_id==Project_members.project_id).where(Project_members.user_id==payload['id']))
    return {"total_projects":total_projects.scalar_one_or_none(),
            'total_tasks':total_tasks.scalar_one_or_none(),
            'total_sprints':total_sprints.scalar_one_or_none(),
            'total_epics':total_epics.scalar_one_or_none()}