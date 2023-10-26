from sqlalchemy import Column, Integer, String, Time
from database import Base

class Places(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String)
    category = Column(String)
    logo = Column(String)
    photos_url = Column(String) #will be list after migration

    monday = Column(String) #Time or Closed
    tuesday = Column(String)
    wednesday = Column(String) 
    thursday = Column(String)
    friday = Column(String)
    saturday = Column(String)
    sunday = Column(String) 

    description = Column(String)
    address = Column(String) #statically typed
    number = Column(String)
    facebook = Column(String)
    instagram = Column(String)
    tiktok = Column(String)
    youtube = Column(String)
    main_price = Column(Integer)
    main_visit = Column(String)
    custom_price = Column(String)
    map_link = Column(String)
    views = Column(Integer)
