from pydantic import BaseModel


class BaseClass(BaseModel):
    name: str
    district: str
    category: str
    logo: str
    description: str
    monday: str
    tuesday: str
    wednesday: str
    thursday: str
    friday: str
    saturday: str
    sunday: str
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
