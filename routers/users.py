from fastapi import  HTTPException, APIRouter
from fastapi.params import Depends, Path
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Annotated
from models import Users
from sqlalchemy.testing.suite.test_reflection import users
from starlette import status
from pydantic import BaseModel,Field
from models import Todos
from database import SessionLocal
from .auth import get_current_user, bcrypt_context

router=APIRouter(
    prefix='/users',
    tags=['users']
)


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]
bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')

class UserVerification(BaseModel):
    password:str
    new_password:str=Field(min_length=6)

class UpdatedPhoneNumber(BaseModel):
    updated_number:str

@router.get('/')
async def get_user(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    return db.query(Users).filter(Users.id==user.get('id')).first()

@router.put('/change_password')
async def change_password(user:user_dependency,db:db_dependency,user_verification:UserVerification):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    user_model=db.query(Users).filter(Users.id==user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password,user_model.hashed_password):
        raise HTTPException(status_code=401,detail="Error on password change")
    user_model.hashed_password=bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()

@router.put('/update_phone_number')
async def update_phone_number(user:user_dependency,db:db_dependency,updatedNumber:UpdatedPhoneNumber):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=404,detail="Item not found")
    user_model.phone_number=updatedNumber.updated_number

    db.add(user_model)
    db.commit()