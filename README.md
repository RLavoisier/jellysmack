# jellysmack
Technical test for jellysmack

# Installation
This application has benn developped and tested with python 3.8.9

## Modules
To install the python modules needed:

`pip install -r rquirements`

## Bdd installation and data importation
For ease of use and test, this application uses SQLite 
To create and feed the database :

`python setup.py`

## Unit tests
Tests use pytest. Launch them with

`py.test`

## Launch the api
The api uses FastApi, launch it using :

`uvicorn api.api:app --reload`

Then access to the doc with :

`http://127.0.0.1:8000/docs`

## Website
For convenience a website is available to see and comment the episodes and character
It uses Flask, you can launch it with :

`python www/app.py`

and access it at http://127.0.0.1:8888/