from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_user_name(db: Session, user_name: str):
    return db.query(models.User).filter(models.User.user_name == user_name).first()

def get_user_by_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_image(db: Session, offer_id: int):
    return db.query(models.Image).filter(models.Image.offer_id == offer_id).first()

def delete_user(db: Session, id: int):
    db.query(models.Image).filter(models.Image.owner_id == id).delete(False)
    db.query(models.Offer).filter(models.Offer.owner_id == id).delete(False)
    db.query(models.User).filter(models.User.id == id).delete(False)
    db.commit()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, 
                            user_name=user.user_name,
                            password=user.password,
                            first_name=user.first_name,
                            last_name=user.last_name, 
                            isAdmin=user.isAdmin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Offer).offset(skip).limit(limit).all()

def get_offer(db: Session, offer_id: int):
    return db.query(models.Offer).filter(models.Offer.id == offer_id).filter().first()

def delete_offer(db: Session, offer_id: int):
    db.query(models.Image).filter(models.Image.offer_id == offer_id).delete(False)
    db.query(models.Offer).filter(models.Offer.id == offer_id).delete(False)
    db.commit()

def get_user_items(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Offer).filter(models.User.id == user_id).offset(skip).limit(limit).all()
    
# def create_user_item(db: Session, offer: models.Offer, user_id: int):
def create_user_item(db: Session, offer: models.Offer):
    db_item = offer
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# best answer i found online for updating data in SQL Alchemy. Prob not the best. 
# ideally, we'd use the native SQL update langauge to do this in the database itself.
# that way it will (probably?) protect us from two users somehow writing data at the same time
# and possibly losing stuff between the two updates. 
def change_user_item(db: Session, old_offer: models.Offer, new_offer: schemas.Offer):
    update_data = new_offer.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(old_offer, key, value)
    db.commit()
    db.refresh(old_offer)
    return old_offer

def change_user_info(db: Session, old_user: models.User, newUser: dict):
    # update_data = newUser.dict(exclude_unset=True)
    for key, value in newUser.items():
        setattr(old_user, key, value)
    db.commit()
    db.refresh(old_user)
    return old_user

def attach_offer_image(db: Session, img: models.Image):
    # db_item = models.Offer(**offer.dict(), owner_id=user_id)
    db_item = img
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_offer_image(db: Session, offer_id: int):
    # db_item = models.Offer(**offer.dict(), owner_id=user_id)
    try:
        db.query(models.Image).filter(models.Image.offer_id == offer_id).delete(False)
        db.commit()
        return True
    except:
        return False
    
