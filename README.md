# Send_IT_APIs
Set of API endpoints to be consumed by a courier service application 

[![Build Status](https://travis-ci.org/dxania/Send_IT_APIs.svg?branch=ft-send-IT-with-database)](https://travis-ci.org/dxania/Send_IT_APIs) 
[![Coverage Status](https://coveralls.io/repos/github/dxania/Send_IT_APIs/badge.svg?branch=ft-send-IT-with-database)](https://coveralls.io/github/dxania/Send_IT_APIs?branch=ft-send-IT-with-database) 
[![Maintainability](https://api.codeclimate.com/v1/badges/8dc6eba4cf7bb21cf416/maintainability)](https://codeclimate.com/github/dxania/Send_IT_APIs/maintainability)


## Features
The API offers the following set of endpoints:


  | REQUEST      | ROUTE                               | FUNCTIONALITY                                                      | PROTECTED  |
  |--------------|-------------------------------------|--------------------------------------------------------------------|------------|
  |  POST        | /auth/signup                        | Register a user                                                    |   NO       |
  |  POST        | /auth/login                         | Login a user                                                       |   NO       |
  |  POST        | /parcels                            | Create a parcel delivery order                                     |   YES      |
  |  GET         | /parcels                            | Fetch all parcel delivery orders                                   |   YES      |
  |  GET         | /parcels/[parcelId]                 | Fetch a specific parcel delivery order                             |   YES      |
  |  GET         | /users/[userId]/parcels             | Fetch all parcel delivery orders by a specific user                |   YES      |
  |  PUT         | /parcels/[parcelId]/destination     | Change the destination of a specific parcel delivery order         |   YES      |
  |  PUT         | /parcels/[parcelId]/present_location| Change the present location of a specific parcel delivery order    |   YES      |
  |  PUT         | /parcels/[parcelId]/status          | Change the status of a specific parcel delivery order              |   YES      |
  |  GET         | /users                              | Fetch all registered users                                         |   YES      |

## Getting started
These instructions will get you a copy of the program on your local machine for development and testing purposes. The instructions are tailored for uses of `LINUX OS` particularly `UBUNTU`

## Prerequisites
What things you will need to run the application

```
Python3
    version: 3.6
```
```
Pip for python3
    $ sudo apt-get install python3-pip
```
```
Flask to build the application
    version: 1.0.2
    $ pip install flask
```
```
Virtualenv to create a virtual environment
    version: 16.0.0
```
```
Pytest to perform tests
    version: 3.9.1
    $ pip install pytest -U
```
Alternatively, run `pip install -r requirements.txt` to install all the necessary tools

## Built With
1. [Flask](http://flask.pocoo.org/) -  microframework for Python
2. [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/latest/)
3. [PostgreSQL](https://www.postgresql.org/) 
4. [Passlib](https://passlib.readthedocs.io/en/stable/install.html)

## Installing
To have a copy of the project on your machine, run the command below in your preferred directory:

``` 
git clone https://github.com/dxania/Send_IT_APIs.git
```
After cloning, you will have a folder named `Send_IT_APIs`

## How to use
1. Navigate to `Send_IT_APIs`
2. Create a virtual environment by running:
``` python3 -m venv <name of virtualenvironment> ```
3. Activate the virtual environment
``` source <name of virtualenvironment>/bin/activate```
You should see the name of the virtual environment placed right before your current path/directory in brackets()
4. Connect to the postgres db
Once Postgres is installed and you can connect, you’ll need to export the DATABASE_URL environment variable for to connect to it when running locally
Run the command below to connect
```
DATABASE_URL=$(heroku config:get DATABASE_URL -a send-it-api-app)
```
5. Run the application
```export FLASK_APP=app.py``` then
```flask run```


## Testing
1. Run `pytest` or `pytest tests/<test_file_name>` in the directory of the project to run unit tests
2. Test with [Postman](https://www.getpostman.com/) by pasting the url [https://send-it-api-app.herokuapp.com/api/v1/auth/signup](http://127.0.0.1:5000/api/v1/auth/signup) (For the POST requests, enter the data as raw application/json)

## Sample Requests and Responses for a non admin user

### Sign up
Endpoint `/api/v1/auth/signup`

Input
```
    {
        "user_name":"Dee",
        "email": "kxania@gmail.com",
        "password":"warmups"
    }
```
Output 
```
{"message":"User Dee successfully created"}
```

### Login
Endpoint `/api/v1/auth/login`

Input
```
    {
        "user_name":"Dee",
        "password":"warmups"
    }
```

Output
```
    {
        "access_token" : some access token,
        "message":"You have sucessfully been logged in as Dee"
    }
```

### Create parcel
Endpoint `/api/v1/parcels`

Input
```
    {
        "recipient_name":"leonne",
        "recipient_mobile": 1234567890,
        "pickup_location":"Entebbe",
        "destination":"Mombasa",
        "weight": 900
    }
```
Output 

```
    {"message":"Parcel successfully created"}
```

### Get the parcel
Endpoint `/api/v1/parcels/1`

Output

```
    {
    "parcel": {
        "created_by": "Dee",
        "destination": "Mombasa",
        "parcel_id": 1,
        "pickup_location": "Entebbe",
        "present_location": "Entebbe",
        "recipient_mobile": "1234567890",
        "recipient_name": "leonne",
        "status": "pending",
        "total_price": 100000,
        "weight": 900
    }
}
```

### Update the destination
Endpoint `/api/v1/parcels/1/destination`

Input
```
    {"destination":"Nairobi"}    
```
Output
```
    {"message":"Destination of parcel 1 changed to Nairobi"}
```

## Deployment
Deployed on [heroku](https://send-it-api-app.herokuapp.com/) 

## Author
[Daizy Obura](https://github.com/dxania/)