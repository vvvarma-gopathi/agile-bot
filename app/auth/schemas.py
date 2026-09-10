from pydantic import BaseModel,EmailStr,Field
from typing import Optional

class UserCreate(BaseModel):
    user_name:str=Field(...,max_length=30,min_length=5)
    name:str=Field(...,max_length=50,min_length=5,pattern="^[a-zA-Z ]+$")
    email:EmailStr=Field(...,max_length=225,min_length=10)
    phone_number:str=Field(...,pattern="^[0-9]{10}$")
    hashed_password:str=Field(...,max_length=25,min_length=8)
    role:str=Field(...,max_length=30,min_length=5,pattern="^[a-zA-Z]+$")

class UserResponse(BaseModel):
    id:int
    user_name:str
    name:str
    email:EmailStr
    phone_number:str
    role:str
    is_active:Optional[bool]=True
    is_deleted:Optional[bool]=False

    class Config:
        orm_mode=True

class UserLogin(BaseModel):
    email:EmailStr=Field(max_length=225,min_length=10)
    hashed_password:str=Field(max_length=25,min_length=8)

class MessageResponse(BaseModel):
    message:str