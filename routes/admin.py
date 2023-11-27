from JWT import create_access_token, USERNAME, PASSWORD, get_current_admin_user
from fastapi import APIRouter, status, Depends, HTTPException, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import UploadFile
from database import get_db
import schemas
import models
import uuid
import os

UPLOAD_FOLDER = "uploads"
BANNER_FOLDER = "banners"


def file_name_generator(filename):
    extension = filename.split(".")[-1]
    random_id = uuid.uuid4()
    return f"{random_id}.{extension}"


def check_authorization(authentic: bool):
    if not authentic:
        return {"details": "Forbidden", "status": status.HTTP_401_UNAUTHORIZED}


router = APIRouter(
    tags=['admin']
)


@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login(response: OAuth2PasswordRequestForm = Depends()):
    if response.username == USERNAME:

        if response.password == PASSWORD:
            access_token = create_access_token(data={"username": USERNAME, "password": PASSWORD})
            return {"access_token": access_token, "token_type": "bearer"}

        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")

    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Username")


@router.post("/places/photo", status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...), authentic: bool = Depends(get_current_admin_user)):

    check_authorization(authentic)

    unique_filename = file_name_generator(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return {"path": f'/{UPLOAD_FOLDER}/{unique_filename}'}


@router.post("/banner", status_code=status.HTTP_201_CREATED)
async def upload_banner(file: UploadFile = File(...), authentic: bool = Depends(get_current_admin_user)):

    check_authorization(authentic)

    unique_filename = file_name_generator(file.filename)
    file_path = os.path.join(BANNER_FOLDER, unique_filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return {'details': 'great success'}

