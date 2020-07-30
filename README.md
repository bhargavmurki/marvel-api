# Marvel-api
An API which gives information about the characters.

# Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

# Prerequisites

What things you need to install the software and how to install them

```
Python 3
virtualenv
```
# Installing

A step by step series of examples that tell you how to get a development env running

1. Clone the repository
```
git clone git@github.com:bhargavmurki/marvel-api.git
```
2. Create virtual environment
```
virtualenv .env
```
3. Activate virtual environment
```
. .env/scripts/activate
```
4. Install the requirements
```
pip install -r requirements.txt
```
5. Create the database
```
export FLASK_APP="path/to/app.py"

flask db_create
```
6. Seed the database
```
flask db_seed
```
7. Run the app
```
flask run 
```
This will run the app on http://127.0.0.1:5000/


# Built With
- [PyCharm CE edition](https://www.jetbrains.com/pycharm/download/#section=windows)
- [Postman](https://www.postman.com/downloads)
- [DB Browser](https://sqlitebrowser.org/dl/)

# Authors
Bhargav Murki (bhargavmurki@gmail.com)

# License
MIT License

Copyright (c) 2020 Bhargav Murki
