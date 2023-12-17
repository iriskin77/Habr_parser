

## How to install

You can install it as a python script

+ Clone the repo

+ Install virtual environment:
  + python -m venv venv
  + .\venv\Scripts\activate (for windows)
  + venv/biv/activate (for linux)

+ Install dependencies: pip install -r requirements.txt

+ Make migrations: python manage.py makemigrations

+ Apply the migrations: python manage.py migrate

+ Create superuser and add links to hubs to db using the admin panel

+ To parse data, make a request to this url: http://127.0.0.1:8000/parse_habr

Description api by swagger: http://127.0.0.1:8000/swagger/

## How it works

#### How api works

The api makes a request to habr.com, takes the necessary data, adds it to the database

![](https://github.com/iriskin77/Habr_parser_api/blob/master/images/api_works.png)

#### How parser works


The parser makes a request to a hub link, then takes all article links which are on the main page of the hub. 
After that the parser makes simultaneous asynchronous requests to all article links, takes data, puts into db. 
Then this cicle repeats until hub links runs out.

![](https://github.com/iriskin77/Habr_parser_api/blob/master/images/parser.png)

## Notes 

Redis, Celery

