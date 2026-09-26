from fastapi import HTTPException,status
from auth.models import Users,Roles
from auth.schemas import UserCreate,UserLogin,MessageResponse,ProfileResponse,SelectUser
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher
from auth.dependencies import create_access_token



#password hashing algorithm with argon2
hasher_algorithm=Argon2Hasher(
    time_cost=2,
    memory_cost=2048,
    parallelism=3
)

#bcrypt password hashing algorithm defining
bcrypt_hasher=BcryptHasher()

password_hasher =PasswordHash((hasher_algorithm, bcrypt_hasher))

def hash_password(password:str)->str:
    return password_hasher.hash(password)

def verify_password(password:str,hash_password:str)->bool:
    return password_hasher.verify(password,hash_password)

def helper_function(user:dict):
    user_details = Users(**user)
    return user_details


def create_user(user:UserCreate,db):
    user_result = db.query(Users).filter(Users.email==user.email).first()
    user_by_user_name=db.query(Users).filter(Users.user_name==user.user_name).first()
    user_by_number=db.query(Users).filter(Users.phone_number==user.phone_number).first()
    if user_result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User with this email or phone number already exists")
    if user_by_user_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User with user name already exists")
    if user_by_number:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User with phone number already exists")
    else:
        user_details = user.model_dump()
        user_details['hashed_password'] = hash_password(user_details['hashed_password'])
        user_details['role_id']=int(user_details['role_id'])
        user_instance = helper_function(user_details)
        db.add(user_instance)
        db.commit()
        db.refresh(user_instance)
        return MessageResponse(message="user registered successfully..")

def authenticate_user(user:UserLogin,db):
    user_result = db.query(Users).filter(Users.email==user.email).first()
    if user_result and verify_password(user.hashed_password,user_result.hashed_password):
        jwt_token=create_access_token({'id':user_result.id,'user_name':user_result.user_name,'role_id':user_result.role_id})
        return {'access_token':jwt_token,'token_type':'bearer'}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid User Credentials')

def profile(payload:dict,db):
    user_result=db.query(Users).filter(Users.id==payload['id']).first()
    print(payload['id'])
    print(user_result,type(user_result))
    return user_result

async def profile_dash(payload,db):
    user=db.query(Users).filter(Users.id==payload['id']).first()
    role=db.query(Roles).filter(Roles.id==user.role_id).first()
    return ProfileResponse(user_name=user.user_name,role=role.name,user_id=user.id)

async def get_users(payload,db):
    if payload['role_id']!=1 and payload['role_id']!=3:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='only a project manager or admin can add project member')
    users=db.query(Users).all()
    if not users:
        return MessageResponse(message='no users found')
    results=[]
    for record in users:
        results.append(SelectUser(user_name=record.user_name,id=record.id))
    return results