from fastapi import APIRouter, Depends, status, HTTPException, Query
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

@router.get('/places', status_code=status.HTTP_200_OK, response_model=List[schemas.Preview])
def filter_and_search(
    query: str = Query(None, description="Search query"),
    category: str = Query(None, description="Category filter"),
    address: str = Query(None, description="Address filter"),
    db: Session = Depends(get_db)
):
    search_conditions = (
        models.Places.name.ilike(f"%{query}%"),
        models.Places.category.ilike(f"%{query}%"),
        models.Places.address.ilike(f"%{query}%")
    )

    places = db.query(models.Places)

    if category:
        places = places.filter(models.Places.category == category)
    if address:
        places = places.filter(models.Places.address == address)
    
    if query:
        places = places.filter(or_(*search_conditions))
    
    places = places.all()

    return places

@router.get("/places/{id}", status_code=status.HTTP_200_OK)
def getID(id:int, db:Session = Depends(get_db)):
    place = db.query(models.Places).filter(models.Places.id == id).first()

    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object Not Found")
    
    return place

@router.get('/text/{page}', status_code=status.HTTP_200_OK)
def getText(page:str):
    try:
        random_text = random.choice(random_texts[page])
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object Not Found")
    
    return {'random text':random_text}

    
@router.get("/banners")
def get_image_paths():
    files = os.listdir(BANNER_FOLDER)

    image_files = [file for file in files if file.lower()]

    image_paths = [f'/{BANNER_FOLDER}/{file}' for file in image_files]

    return {"banners":image_paths}