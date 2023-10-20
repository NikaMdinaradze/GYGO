from pydantic import BaseModel


#schema of places in the preview
class Preview(BaseModel):
    id:int
    name: str
    # address: str
    category: str
    logo: str
    description: str
    monday :str #Time or Closed
    tuesday : str
    wednesday :str
    thursday : str
    friday : str
    saturday : str
    sunday : str
    class Config():
        form_attributes = True

#schema with essential descriptions of place
class UploadPlaces(BaseModel):
    name: str
    category: str
    logo: str
    description: str
    main_price: int
    main_visit: str
    photos_url: str #will be list after migration
    monday :str #Time or Closed
    tuesday : str
    wednesday :str
    thursday : str
    friday : str
    saturday : str
    sunday : str
    address: str
    number: str
    facebook: str
    instagram: str
    tiktok: str
    youtube: str
    custom_price: str
    map_link: str
    views: int

    class Config():
        form_attributes = True

class Login(BaseModel):
    username:str
    password:str
