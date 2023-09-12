from fastapi import APIRouter, status, Depends, HTTPException, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from JWT import create_access_token, USERNAME, PASSWORD, get_current_admin_user
from fastapi import UploadFile
from sqlalchemy.orm import Session
import schemas
import models
from database import get_db
import uuid
import os

UPLOAD_FOLDER = "uploads"
BANNER_FOLDER = "banners"

def FileNameGenerator(filename):
    extension = filename.split(".")[-1]
    id = uuid.uuid4()
    return f"{id}.{extension}"

router = APIRouter(
    tags=['admin']
)


@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login(response:OAuth2PasswordRequestForm = Depends()):
    if response.username == USERNAME:

        if response.password == PASSWORD:
            access_token = create_access_token(data={"username":USERNAME, "password":PASSWORD})
            return {"access_token":access_token, "token_type":"bearer"}
        
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")
    
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Username")

@router.post("/upload", status_code=status.HTTP_201_CREATED)
def upload(response: schemas.UploadPlaces, db: Session = Depends(get_db), authentic: bool = Depends(get_current_admin_user)):
    new_place = models.Places(
        name=response.name,
        category=response.category,
        logo=response.logo,
        photos_url=response.photos_url,
        monday = response.monday,
        tuesday = response.tuesday,
        wednesday = response.wednesday,
        thursday = response.thursday,
        friday = response.friday,
        saturday = response.saturday,
        sunday = response.sunday,
        description=response.description,
        address=response.address,
        number=response.number,
        facebook=response.facebook,
        main_price=response.main_price,
        main_visit=response.main_visit,
        custom_price=response.custom_price,
        map_link=response.map_link,
        views=response.viewvs
    )
    db.add(new_place)
    db.commit()
    db.refresh(new_place)
    return new_place
    

@router.post("/photo_upload/", status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...),authentic: bool = Depends(get_current_admin_user)):
    unique_filename = FileNameGenerator(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return {"path":f'/{UPLOAD_FOLDER}/{unique_filename}'}

@router.post("/upload_banner/", status_code=status.HTTP_201_CREATED)
async def upload_banner(file: UploadFile = File(...),authentic: bool = Depends(get_current_admin_user)):
    unique_filename = FileNameGenerator(file.filename)
    file_path = os.path.join(BANNER_FOLDER, unique_filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return {'details':'great success'}



@router.put("/update/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id:int,response:schemas.UploadPlaces, db:Session = Depends(get_db),authentic: bool = Depends(get_current_admin_user)):
    place = db.query(models.Places).filter(models.Places.id == id).first()

    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object Not Found")
    
    place.name = response.name
    place.category = response.category
    place.logo = response.logo
    place.photos_url = response.photos_url
    place.monday = response.monday
    place.tuesday = response.tuesday
    place.wednesday = response.wednesday
    place.thursday = response.thursday
    place.friday = response.friday
    place.saturday = response.saturday
    place.sunday = response.sunday
    place.description = response.description
    place.address = response.address
    place.number = response.number
    place.facebook = response.facebook
    place.main_price = response.main_price
    place.main_visit = response.main_visit
    place.custom_price = response.custom_price
    place.map_link = response.map_link
    place.views = response.viewvs

    db.commit()
    db.refresh(place)
    return place
     
@router.delete('/delete/{id}',status_code=status.HTTP_202_ACCEPTED)
def delete(id:int, db:Session = Depends(get_db),authentic: bool = Depends(get_current_admin_user)):
    place = db.query(models.Places).filter(models.Places.id==id)
    if not place.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object Not Found")
    
    place.delete(synchronize_session = False)
    db.commit()
    return {"detail":f"Object {id} Deleted"}
