from fastapi import APIRouter, Depends, status, HTTPException
import schemas, models
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import or_
import random
import os
from typing import List
from .admin import BANNER_FOLDER

router = APIRouter(
    tags=['user']
)

random_texts = {
    'home':['სალამი, მეგობარო!', 'ძმას ვეჭიდავე'],
    'search':['მოძებნე შენთვის სასურველი ადგილი გასართობად', 'წადი საცა გინდა'],
    'product': ['გაიკითხე ამაზე იაფად თუ ნახე, მოდი და დაგიკლებ', 'კარგი არჩევანია']
}

@router.get('/search', status_code=status.HTTP_200_OK, response_model=List[schemas.Preview])
def search(query:str, db:Session = Depends(get_db)):

    search_conditions = (
        models.Places.name.ilike(f"%{query}%"),
        models.Places.category.ilike(f"%{query}%"),
        models.Places.address.ilike(f"%{query}%")
    )

    places = db.query(models.Places).filter(or_(*search_conditions)).all()

    return places

@router.get('/get_all', status_code=status.HTTP_200_OK, response_model=List[schemas.Preview])
def get_all(db:Session = Depends(get_db)):
    places = db.query(models.Places).all()
    return places

@router.get("/get/{id}", status_code=status.HTTP_200_OK)
def getID(id:int, db:Session = Depends(get_db)):
    place = db.query(models.Places).filter(models.Places.id == id).first()

    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object Not Found")
    
    return place

@router.get('/text_gen/{page}}', status_code=status.HTTP_200_OK)
def getText(page):
    try:
        random_text = random.choice(random_texts[page])
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object Not Found")
    
    return {'random text':random_text}



@router.get('/filter_by', status_code=status.HTTP_200_OK)
def filter(db:Session = Depends(get_db),category:str = None, address:str = None):
    places = db.query(models.Places)
    if  category:
        places = places.filter(models.Places.category == category)
    if  address:
        places = places.filter(models.Places.address == address)

    if places:
            places = places.all()
            
    return places
    
@router.get("/get_banners")
def get_image_paths():
    files = os.listdir(BANNER_FOLDER)

    image_files = [file for file in files if file.lower()]

    image_paths = [f'/{BANNER_FOLDER}/{file}' for file in image_files]

    return {"banners":image_paths}