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


@router.post("/places", status_code=status.HTTP_201_CREATED)
def upload(response: schemas.Places, db: Session = Depends(get_db),
           authentic: bool = Depends(get_current_admin_user)):

    check_authorization(authentic)

    new_place = models.Places(**response.__dict__)
    db.add(new_place)
    db.commit()
    db.refresh(new_place)
    return {"details": "Place Has Uploaded", "status": status.HTTP_201_CREATED}


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


@router.put("/places/{place_id}", status_code=status.HTTP_202_ACCEPTED)
def update(place_id: int, response: schemas.Places, db: Session = Depends(get_db),
           authentic: bool = Depends(get_current_admin_user)):

    check_authorization(authentic)

    place = db.query(models.Places).filter(models.Places.id == place_id).first()
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object Not Found")
    dict_response = response.__dict__

    for key, value in dict_response.items():
        setattr(place, key, value)

    db.commit()
    return {"details": f"Place {place_id} Has Updated", "status": status.HTTP_202_ACCEPTED}


@router.delete('/places/{place_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(place_id: int, db: Session = Depends(get_db), authentic: bool = Depends(get_current_admin_user)):
    place = db.query(models.Places).filter(models.Places.id == place_id)

    check_authorization(authentic)

    photos = place.first().photos_url.split(',')
    photos.append(place.first().logo)

    for photo in photos:
        if photo:
            file_path = os.path.join(UPLOAD_FOLDER, os.path.basename(photo))
            if os.path.exists(file_path):
                os.remove(file_path)

    place.delete()
    db.commit()
    return {"detail": f"Object {id} Deleted"}
