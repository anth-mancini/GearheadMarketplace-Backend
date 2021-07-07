from fastapi.middleware.cors import CORSMiddleware

from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import null
from pydantic import BaseModel

from sql import crud, models, schemas
from sql.database import SessionLocal, engine

# AWS S3 
from botocore.client import BaseClient
from botocore.exceptions import ClientError
from s3.deps import s3_auth
from s3.upload import upload_file_to_bucket
from enum import Enum

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "localhost:8888",
    "http://localhost:8888",
    "http://localhost:8000",
    "localhost:8000",
    "localhost",
    "localhost:80",
    "http://localhost",
    "http://localhost:80",
    "https://gearheadmarketplace.herokuapp.com",
    "gearheadmarketplace.herokuapp.com",
    "https://www.gearheadmarketplace.herokuapp.com",
    "www.gearheadmarketplace.herokuapp.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}

@app.get("/status")
async def return_server_status():
    if engine != null:
        return "online"
    return "offline"

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


# testing AWS S3
@app.get("/buckets")
def get_buckets(s3: BaseClient = Depends(s3_auth)):
    response = s3.list_buckets()
    return response['Buckets']

@app.get("/buckets/list")
def get_list_of_buckets(s3: BaseClient = Depends(s3_auth)):
    response = s3.list_buckets()
    buckets = []

    for bucket in response['Buckets']:
        buckets.append(bucket['Name'])
        # print(bucket['Name'])

    # BucketName = Enum('BucketName', buckets)
    return buckets

@app.get("/buckets/getImage" , status_code=status.HTTP_201_CREATED, summary="Upload files to AWS S3 Buckets",
             description="Upload a valid file to AWS S3 bucket", name="Get files from AWS S3",
             response_description="Successfully uploaded file to S3 bucket")
def get_list_of_buckets(bucket: str, folder: str, s3: BaseClient = Depends(s3_auth)):
    response = s3.list_buckets()
    buckets = []

    for bucket in response['Buckets']:
        buckets.append(bucket['Name'])
        # print(bucket['Name'])

    # BucketName = Enum('BucketName', buckets)
    return buckets
@app.post("/buckets/upload", status_code=status.HTTP_201_CREATED, summary="Upload files to AWS S3 Buckets",
             description="Upload a valid file to AWS S3 bucket", name="POST files to AWS S3",
             response_description="Successfully uploaded file to S3 bucket")
def upload_file(folder: str, bucket: str, s3: BaseClient = Depends(s3_auth), file_obj: UploadFile = File(...)):
    upload_obj = upload_file_to_bucket(s3_client=s3, file_obj=file_obj.file,
                                       bucket=bucket,
                                       folder=folder,
                                       object_name=file_obj.filename
                                       )
    if upload_obj:
        return JSONResponse(content="Object has been uploaded to bucket successfully",
                            status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="File could not be uploaded")

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = Depends(s3_auth)
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response