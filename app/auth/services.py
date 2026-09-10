from fastapi import HTTPException,status
from core.models import Users
from auth.schemas import UserCreate,UserLogin
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

hasher_algorithm=Argon2Hasher(
    time_cost=2,
    memory_cost=2048,
    parallelism=3
)
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
    user_result = db.query(Users).filter(Users.email==user.email or Users.user_name==user.user_name).first()
    if user_result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User with this email or phone number already exists")
    else:
        user_details = user.model_dump()
        user_details['hashed_password'] = hash_password(user_details['hashed_password'])
        user_instance = helper_function(user_details)
        db.add(user_instance)
        db.commit()
        db.refresh(user_instance)
        return user_instance

def authenticate_user(user:UserLogin,db):
    user_result = db.query(Users).filter(Users.email==user.email).first()
    if user_result and verify_password(user.hashed_password,user_result.hashed_password):
        return {'message':"User Login Successfull"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid User Credentials')