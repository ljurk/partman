# partman

## Part Managment tool

* built with docker
    * postgres
    * python
    * php
* cli with python


just build

    docker-compose up --build

and run

    docker-compose up

you can see your api under

    http://localhost:5001

and your website under

    http://localhost:5000

supported Methods
* GET
* PUT
* DELETE
* PATCH

GET

    GET /parts

    GET /parts?id=1

    GET /parts
    {
        "id": 1
    }

PUT
dont put an id into PUT, the id is an auto-increment

    PUT /parts
    {
        "name": "100k",
        "categoryId": 1,
        "description: "test",
        "amount": 23
    }

    PUT /categories
    {
        "name": "resistor"
    }

DELETE

    DELETE /parts
    {
        "id": 5
    }

PATCH
actualy only for amounts

    PATCH /parts
    {
        "id": 1,
        "amount": 303
    }




TODO:

* EDIT,DELETE in website
* PUT,EDIT,DELETE in cli
* ssl proxy with nginx
