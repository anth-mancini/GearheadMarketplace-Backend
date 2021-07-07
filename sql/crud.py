from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_user_name(db: Session, user_name: str):
    return db.query(models.User).filter(models.User.user_name == user_name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, 
                            user_name=user.user_name,
                            password=user.password,
                            first_name=user.first_name,
                            last_name=user.last_name, 
                            level=user.level)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Offer).offset(skip).limit(limit).all()

def get_user_items(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Offer).filter(models.User.id == user_id).offset(skip).limit(limit).all()
    
# def create_user_item(db: Session, offer: models.Offer, user_id: int):
def create_user_item(db: Session, offer: models.Offer):
    # db_item = models.Offer(**offer.dict(), owner_id=user_id)
    db_item = offer
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def attach_offer_image(db: Session, img: models.Image):
    # db_item = models.Offer(**offer.dict(), owner_id=user_id)
    db_item = img
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
