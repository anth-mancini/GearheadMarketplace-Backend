from sql.database import Base
from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.schema import Column

class ImageBase(BaseModel):
    link: str

class ImageCrate(ImageBase):
    pass

class Image(ImageBase):
    id: int
    offer_id: int
    owner_id: int
    class Config:
        orm_mode = True
        
class OfferBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    location: Optional[str] = None
    shipping_availability: Optional[bool] = None


class OfferCreate(OfferBase):
    pass

class Offer(OfferBase):
    id: int
    owner_id: int
    images: List[Image] = []
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str

class UserBase(BaseModel):
    email: str
    user_name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    isAdmin: Optional[bool] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    offers: List[Offer] = []

    class Config:
        orm_mode = True

