from fastapi_storages.integrations.sqlalchemy import ImageType
from fastapi_storages import FileSystemStorage
from sqlalchemy import Column, Integer, String, Time, Text, Float
from database import Base

storage = FileSystemStorage(path="/tmp")


class Places(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    logo = Column(ImageType(storage=storage), nullable=False)
    photos_url = Column(String)  # is not list instead , are separators

    monday_open = Column(Time)
    monday_close = Column(Time)
    tuesday_open = Column(Time)
    tuesday_close = Column(Time)
    wednesday_open = Column(Time)
    wednesday_close = Column(Time)
    thursday_open = Column(Time)
    thursday_close = Column(Time)
    friday_open = Column(Time)
    friday_close = Column(Time)
    saturday_open = Column(Time)
    saturday_close = Column(Time)
    sunday_open = Column(Time)
    sunday_close = Column(Time)

    description = Column(Text, nullable=False)
    district = Column(String, nullable=False)
    full_address = Column(String, nullable=False)

    number = Column(String)
    facebook = Column(String)
    instagram = Column(String)
    tiktok = Column(String)
    youtube = Column(String)
    discord = Column(String)
    telegram = Column(String)

    main_price = Column(Float, nullable=False)
    main_visit = Column(String, nullable=False)
    custom_price = Column(String)
    map_link = Column(String)
    views = Column(Integer, default=0, nullable=False)

