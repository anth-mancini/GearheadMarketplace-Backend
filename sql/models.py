from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    isAdmin = Column(Boolean)
    offers = relationship("Offer", back_populates="owner")

class Offer(Base):
    __tablename__ = "offers"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    price = Column(Float)
    location = Column(String)
    description = Column(String)
    shipping_availability = Column(Boolean)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="offers")
    images = relationship("Image", back_populates="offers")

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    link = Column(String)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    offers = relationship("Offer", back_populates="images")
# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")