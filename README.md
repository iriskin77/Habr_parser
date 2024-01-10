## What is this?

The main idea is to create cron-parsers which can periodically collect new articles
from different sites using API. So, this project is an api (Django REST) for parsers that collect data (articles) from the following sites:

+ mel.fm https://mel.fm/
+ habr.com https://habr.com/ru/
+ tinkoff-journal https://journal.tinkoff.ru/


## How it works


#### How api works

POST request from the server runs the parsers:

+ api/v1/pars_habr runs the parser for habr.com
+ api/v1/pars_mel runs the parser for mel.fm
+ api/v1/pars_tink runs the parser for tinkoff-journal

A parser sequentially collects articles from all categories which added into database.
For example, for habr.com we can insert into database such categories as programming and math, using django-admin.
Then the parser will collect articles from the main page of the hub dedicated to programming and math and insert into database. 
After that other services can get the data useing API. If a service sets a timer, then the parser can do it every 1/2/3 hours/days/weeks. 
You can see it in the schema:

![](https://github.com/iriskin77/Habr_parser_api/blob/master/images/dj_pars.png)

#### How parsers work

All parsers work approximately in the same way. A parser receives a number of links to categories, for example,
math/machine learning for the parser which parses habr.com or school/education for mel-parser. After that the parser
consistently collects articles from each category. You can see it in the schema:

![](https://github.com/iriskin77/Habr_parser_api/blob/master/images/parser.png)

## How to install

Now it is possible to install it only as a python script:

+ Clone the repo

+ Install virtual environment:
  + python -m venv venv
  + .\venv\Scripts\activate (for windows)
  + source venv/biv/activate (for linux)

+ Install dependencies: pip install -r requirements.txt

+ Make migrations: python manage.py makemigrations

+ Apply the migrations: python manage.py migrate

+ Create superuser and add links to hubs to db using the admin panel

+ Install Celery and Redis

Description api by swagger: swagger/

## Notes 

There are things to do:

+ Dockerfile to install the project in a simpler way. Now it is quit difficult to do...
+ Maybe deploying the project in a server
