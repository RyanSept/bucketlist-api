# BucketList-API

[![Build Status](https://travis-ci.org/RyanSept/bucketlist-api.svg?branch=develop)](https://travis-ci.org/RyanSept/bucketlist-api)
[![Coverage Status](https://coveralls.io/repos/github/RyanSept/bucketlist-api/badge.svg?branch=develop)](https://coveralls.io/github/RyanSept/bucketlist-api?branch=develop)

This is an API that provides access to a bucketlist.

## Dependencies

 - Flask-JWT - a Flask extension that simplifies JSON token based authentication.
 - Flask - A python web framework.
 - SQLAlchemy - a python orm.

##Installation
To install first navigate to the directory of your choice on your computer and run `git clone https://github.com/RyanSept/bucketlist-api.git` .

Change into the app directory by running `cd BucketList`.

After successfully doing this, call `git checkout develop` .

Install the requirements using `pip install -r requirements.txt`.


##Testing 
Use nosetests to run tests (with coverage) like this: `nosetests --with-coverage --cover-package=app`

##Usage

You can run the application with `python manage.py`

| EndPoint                            | Allowed Methods  | Functionality                                    | Requires Token |
|-------------------------------------|------------------|--------------------------------------------------|----------------|
| `/auth/login`                       | POST             | Logs a user in                                   | No             |
| `/auth/register`                    | POST             | Register a user                                  | No             |
| `/bucketlists`                      | POST, GET        | Create a retrieve all bucket lists               | Yes            |
| `/bucketlists/<id>`                 | GET, PUT, DELETE | Retrieve, update and delete a single bucket list | Yes            |
| `/bucketlists/<id>/items`           | POST             | Create a new item in bucket list                 | Yes            |
| `/bucketlists/<id>/items/<item_id>` | PUT, DELETE      | Delete an item in a bucket list                  | Yes            |




