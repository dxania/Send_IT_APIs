# Send_IT_APIs
Set of API endpoints to be consumed by a courier service application 

<!-- [![Build Status](https://travis-ci.com/dxania/Store_Manager_APIs.svg?branch=develop)](https://travis-ci.com/dxania/Store_Manager_APIs)
[![Coverage Status](https://coveralls.io/repos/github/dxania/Store_Manager_APIs/badge.svg?branch=develop)](https://coveralls.io/github/dxania/Store_Manager_APIs?branch=develop)
[![Code Climate](https://codeclimate.com/github/codeclimate/codeclimate/badges/gpa.svg)](https://codeclimate.com/github/dxania/Store_Manager_APIs) -->

[![Build Status](https://travis-ci.org/dxania/Send_IT_APIs.svg?branch=feature)](https://travis-ci.org/dxania/Send_IT_APIs)


## Features
The Program offers the following set of endpoints:


  | REQUEST           | ROUTE                      | FUNCTIONALITY                                      |
  |-------------------|----------------------------|----------------------------------------------------|
  |  GET              | /parcels                   | Fetch all parcel delivery orders                   |
  |  GET              | /parcels/[parcelId]        | Fetch a specific parcel delivery order             |                     
  |  GET              | /users/[userId]/parcels    | Fetch all parcel delivery orders by a specific user|                  
  |  PUT              | /parcels/[parcelId]/cancel | Cancel a specific parcel delivery order            | 
  |  POST             | /parcels                   | Create a parcel delivery order                     | 



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
[Flask](http://flask.pocoo.org/) -  microframework for Python

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
4. Run the application
```export FLASK_APP=app.py``` then
```flask run```
5. Follow the instructions

## Testing
1. Run `pytest` or `pytest tests/<test_file_name>` in the directory of the project to run unit tests
2. Test with [Postman](https://www.getpostman.com/) by pasting the url [http://127.0.0.1:5000/api/v1/parcels](http://127.0.0.1:5000/api/v1/parcels) as Admin or [http://127.0.0.1:5000/api/v1/users/parcels](http://127.0.0.1:5000/api/v1/sales/parcels) as a specific user into the url section and call the GET/POST methods accordingly. (For the POST requests, enter the data as raw application/json)

## Deployment
Deployed on heroku.
Visit the this [link](https://send-it-apis.herokuapp.com) to interact with the deployed app

## Author
[Daizy Obura](https://github.com/dxania/)