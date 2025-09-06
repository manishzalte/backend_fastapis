from jose import  jwt,ExpiredSignatureError,JWTError
from datetime import datetime , timedelta,timezone 
from Schema.schema import  TokenData
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from concel_data.database import get_db
from Schema import model
from sqlalchemy.orm import Session
import os 
from concel_data.config import setting
SECRET_KEY = setting.SECRET_KEY
ALGORITHM = setting.ALGORITHM

ACCESS_TOKEN_EXPIRE_MINTUES = setting.ACCESS_TOKEN_EXPIRE_MINTUES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINTUES)
    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encode_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,ALGORITHM)
        id = str(payload.get("user_id"))
        if id is None or id == None:
            raise credentials_exception
        token_data = TokenData(id= id)
        return token_data
    except ExpiredSignatureError:
        raise credentials_exception
    except JWTError: 
        raise credentials_exception
    

def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,detail= "Could not verify credentials ",headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token,credentials_exception)
    user = db.query(model.User).filter(model.User.id == token.id).first()
    return user
