We'll use Heroku at the end of it all to deploy the main branch of the PHP app and FastAPI

FastAPI: https://medium.com/fastapi-tutorials/deploying-fastapi-to-heroku-cd00bdcf3be4

PHP: https://devcenter.heroku.com/articles/deploying-php

How to run this: 

The backend uses FastAPI, that is Python based so you want to make sure you have Python3.9 installed

We are using a virtual environment to install fastapi and uvicorn. So here's how you'd run spin up this server:

make sure to run this inside the "backend" folder. Then open a terminal and run:

$ python3.9 -m venv venv
$ source venv/bin/activate
$ export PYTHONPATH=$PWD

it should be installed already but if it doesnt work: 

pip install fastapi uvicorn

to start the server make sure you are in the backend folder again, and run:

python main.py

You're done. Go and check "localhost:8000" to make sure it worked. 

Now for the PHP app:

Get a AMP for whatever system you're using and follow the steps for integrating this into phpStorm: 

https://www.jetbrains.com/help/phpstorm/installing-an-amp-package.html

recommend getting phpStorm and link your amp. You can get the deluxe ;) addition if you use your windsor account.

Before you start your MAMP server, point the root dir to the dir of the PHP app. 

For me it's something like this: Users ▹ felixi ▹ PhpstormProjects ▹ GearheadMarketplace-Frontend
