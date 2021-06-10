from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
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