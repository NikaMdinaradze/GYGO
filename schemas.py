from pydantic import BaseModel, HttpUrl


class BaseClass(BaseModel):
    name: str
    district: str
    category: str
    logo: str
    description: str
    monday_open: str
    monday_close: str
    tuesday_open: str
    tuesday_close: str
    wednesday_open: str
    wednesday_close: str
    thursday_open: str
    thursday_close: str
    friday_open: str
    friday_close: str
    saturday_open: str
    saturday_close: str
    sunday_open: str
    sunday_close: str
    main_price: int
    main_visit: str
    photos_url: str


class Preview(BaseClass):
    id: int

    class Config:
        form_attributes = True


class Places(BaseClass):
    full_address: str
    number: str
    facebook: str
    instagram: str
    tiktok: str
    youtube: str
    discord: str
    telegram: str
    custom_price: str
    map_link: str
    views: int

    class Config:
        form_attributes = True


class Login(BaseModel):
    username: str
    password: str
