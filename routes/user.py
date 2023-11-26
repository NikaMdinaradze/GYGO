from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from .admin import BANNER_FOLDER
from database import get_db
from sqlalchemy import or_
from typing import List
import schemas
import models
import random
import os


router = APIRouter(
    tags=['user']
)

random_texts = {
    'home': ['სალამი, მეგობარო!', 'ძმას ვეჭიდავე'],
    'search': ['მოძებნე შენთვის სასურველი ადგილი გასართობად'],
    'product': ['გაიკითხე ამაზე იაფად თუ ნახე, მოდი და დაგიკლებ', 'კარგი არჩევანია!']
}


@router.get('/places', status_code=status.HTTP_200_OK, response_model=List[schemas.Preview])
def filter_and_search(
        query: str = Query(None, description="Search query"),
        category: str = Query(None, description="Category filter"),
        district: str = Query(None, description="Address filter"),
        max_price: float = Query(None, description="Price filter"),
        min_price: float = Query(None, description="Price filter"),
        db: Session = Depends(get_db)
):
    search_conditions = (
        models.Places.name.ilike(f"%{query}%"),
        models.Places.category.ilike(f"%{query}%"),
        models.Places.district.ilike(f"%{query}%")
    )

    places = db.query(models.Places)

    if category:
        places = places.filter(models.Places.category == category)
    if district:
        places = places.filter(models.Places.district == district)
    if max_price:
        places = places.filter(models.Places.main_price <= max_price)
    if min_price:
        places = places.filter(models.Places.main_price >= min_price)
    if query:
        places = places.filter(or_(*search_conditions))

    places = places.all()

    return places


@router.get("/places/{place_id}", status_code=status.HTTP_200_OK)
def get_id(place_id: int, db: Session = Depends(get_db)):
    place = db.query(models.Places).filter(models.Places.id == place_id).first()

    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object Not Found")

    place.views += 1
    db.commit()
    db.refresh(place)
    return place


@router.get('/text', status_code=status.HTTP_200_OK)
def get_text(page: str):
    """use home, search or product in get request"""
    texts = random_texts.get(page)

    if not texts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object Not Found")

    random_text = random.choice(texts)
    return {'random text': random_text}


@router.get("/banners")
def get_image_paths():
    files = os.listdir(BANNER_FOLDER)

    image_files = [file for file in files if file.lower()]

    image_paths = [f'/{BANNER_FOLDER}/{file}' for file in image_files]

    return {"banners": image_paths}
