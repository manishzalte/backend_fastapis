from fastapi import status, HTTPException, Response,Depends, APIRouter
from Schema.schema import UserBase, User
from concel_data.utils import passhash
from typing import List
from concel_data.database import  get_db
from Schema import model
from sqlalchemy.orm import Session
from concel_data.oauth import get_current_user

router = APIRouter(prefix= "/user", tags=['users'])

@router.post("/", status_code= status.HTTP_201_CREATED, response_model=UserBase)
async def create_user(payload: User, db:Session = Depends(get_db)):
    # hash the password  - payload.password
    check_user_in_system = db.query(model.User).filter(model.User.email == payload.email)
    if check_user_in_system.first() is not None:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail= f"User {payload.email} already exist please checkpassword or use different email to login")
    hashed_password = passhash(payload.password)
    payload.password = hashed_password
    new_user = model.User(**payload.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", status_code=status.HTTP_200_OK,response_model=List[UserBase])
async def get_user(id: int, db:Session = Depends(get_db),current_user:int =Depends(get_current_user)):
   user_exists = db.query(model.User).filter(model.User.id == id)
   if user_exists.first() is None:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"The user id : {id } was not found ")
   return user_exists

@router.delete('/', status_code= status.HTTP_204_NO_CONTENT)
async def delete_user_from_db(db:Session = Depends(get_db), current_user:int = Depends(get_current_user)):
    delete_query = db.query(model.User).filter(model.User.id == current_user.id).first()
    if delete_query is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="user not found")
    if delete_query.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid user")
    db.delete(delete_query)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


