from fastapi import Depends,status,APIRouter
from auth.schemas import UserCreate,UserResponse,UserLogin,TokenResponse,MessageResponse,ProfileResponse,SelectUser
from auth.services import create_user,authenticate_user,profile,profile_dash,get_users
from core.database import get_db
from auth.dependencies import user_form,get_current_user,user_login_form
from typing import Annotated


auth_router = APIRouter(prefix="/auth",tags=["AUTHENTICATION"])

@auth_router.post("/register",response_model=MessageResponse,status_code=status.HTTP_201_CREATED)
def register_user(user:Annotated[UserCreate,Depends(user_form)],db=Depends(get_db)):
    return create_user(user=user,db=db)

@auth_router.post("/login",response_model=TokenResponse,status_code=status.HTTP_200_OK)
def login_user(user:Annotated[UserLogin,Depends(user_login_form)],db=Depends(get_db)):
    return authenticate_user(user=user,db=db)

@auth_router.get("/profile",response_model=UserResponse,status_code=status.HTTP_200_OK)
def get_profile(payload:dict=Depends(get_current_user),db=Depends(get_db)):
    return profile(payload,db)

@auth_router.get("/profile/dash",response_model=ProfileResponse,status_code=status.HTTP_200_OK)
async def get_profile_dash(payload:dict=Depends(get_current_user),db=Depends(get_db)):
    return await profile_dash(payload,db)

@auth_router.get('/select/users',response_model=list[SelectUser],status_code=status.HTTP_200_OK)
async def display_users(payload=Depends(get_current_user),db=Depends(get_db)):
    return await get_users(payload,db)