from fastapi import Depends,status,APIRouter
from auth.schemas import UserCreate,UserResponse,UserLogin,MessageResponse
from auth.services import create_user,authenticate_user
from core.database import get_db

auth_router = APIRouter(prefix="/auth",tags=["AUTHENTICATION"])

@auth_router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register_user(user:UserCreate,db=Depends(get_db)):
    return create_user(user=user,db=db)

@auth_router.post("/login",response_model=MessageResponse,status_code=status.HTTP_200_OK)
def login_user(user:UserLogin,db=Depends(get_db)):
    return authenticate_user(user=user,db=db)