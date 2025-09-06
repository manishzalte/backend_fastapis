from fastapi import APIRouter,Depends, HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from concel_data.database import get_db 
from Schema.schema import UserLogin
from Schema import model
from concel_data import utils,oauth

router = APIRouter()

@router.post("/login")
async def login (user_cred : OAuth2PasswordRequestForm =Depends(),db: Session= Depends(get_db)):
    user = db.query(model.User).filter(model.User.email == user_cred.username).first()
    if not user: 
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Invalid creds please check the password or email")
    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invaild creds")
    access_token = oauth.create_access_token(data={"user_id":str(user.id)})
    return{"token": access_token, "token_type":"Bearer"}

