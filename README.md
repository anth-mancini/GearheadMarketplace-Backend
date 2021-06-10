# GearheadMarketplace
 
How to run this: 

The backend uses FastAPI, that is Python based so you want to make sure you have Python3.9 installed

Here's how you'd run spin up this server in a local virtual env:

open a terminal and run:

python3.9 -m venv venv
source venv/bin/activate
export PYTHONPATH=$PWD

to start the server make sure you are in the backend folder again, and run:

python main.py

You're done. Go and check "localhost:8000" to make sure it worked.

Dependcines:

fastapi
uvicorn
gunicorn
uvloop
httptools
