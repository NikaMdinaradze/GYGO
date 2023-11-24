from datetime import timedelta, datetime
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends
from typing import Annotated
from schemas import Login
from dotenv import load_dotenv
import os


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
USERNAME = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        user = jwt.decode(token, SECRET_KEY, ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_admin_user(
    current_user: Annotated[Login, Depends(get_current_user)]
):
    if current_user['username'] == USERNAME and current_user['password'] == PASSWORD:
        return True
    
    raise HTTPException(status_code=400, detail="Incorrect username or password")
