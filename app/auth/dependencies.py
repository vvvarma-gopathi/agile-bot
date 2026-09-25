from fastapi import HTTPException,status,Form,Depends
from core.config import settings
import jwt
from typing import Annotated
from auth.schemas import UserCreate,UserLogin
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta,timezone
from core.config import settings
import jwt

auth_bearer=OAuth2PasswordBearer(tokenUrl='login')

def user_form(
        user_name:Annotated[str,Form()],
        name:Annotated[str,Form()],
        password:Annotated[str,Form()],
        email:Annotated[str,Form()],
        role_id:Annotated[int,Form()],
        phone_number:Annotated[str,Form()]
):
    return UserCreate(
        user_name=user_name,
        name=name,
        email=email,
        phone_number=phone_number,
        hashed_password=password,
        role_id=role_id
    )

def user_login_form(
        email:Annotated[str,Form()],
        password:Annotated[str,Form()]
):
    return UserLogin(
        email=email,
        hashed_password=password
    )

#decoding jwt token sent by the client and returing the dict
def get_current_user(token:str=Depends(auth_bearer))->dict:
    try:
        payload=jwt.decode(
            token,
            settings.JWT_SecretKey,
            algorithms=[settings.JWT_Hashing_Algorithm]
        )
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invaid Token')
        else:
            return payload
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid Token')

#function for creating JWT token
def create_access_token(data:dict):
    expire=datetime.now(timezone.utc)+timedelta(minutes=30)
    payload={
        'id':str(data['id']),
        'user_name':data['user_name'],
        'role_id':data['role_id'],
        'exp':expire
    }
    token=jwt.encode(
        payload,
        settings.JWT_SecretKey,
        algorithm=settings.JWT_Hashing_Algorithm
    )
    print(token,type(token))
    return token


#validate_users
def validate_user(payload):
    if not payload['id']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid user credentials please login to continue..')
    