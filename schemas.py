from pydantic import BaseModel


class BaseClass(BaseModel):
    name: str
    district: str
    category: str
    logo: str
    description: str
    monday_open: str | None
    monday_close: str | None
    tuesday_open: str | None
    tuesday_close: str | None
    wednesday_open: str | None
    wednesday_close: str | None
    thursday_open: str | None
    thursday_close: str | None
    friday_open: str | None
    friday_close: str | None
    saturday_open: str | None
    saturday_close: str | None
    sunday_open: str | None
    sunday_close: str | None
    main_price: int
    main_visit: str
    photos_url: str


class Preview(BaseClass):
    id: int

    class Config:
        form_attributes = True


class Places(BaseClass):
    full_address: str
    number: str | None
    facebook: str | None
    instagram: str | None
    tiktok: str | None
    youtube: str | None
    discord: str | None
    telegram: str | None
    custom_price: str | None
    map_link: str | None
    views: int

    class Config:
        form_attributes = True


class Login(BaseModel):
    username: str
    password: str
