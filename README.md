+ [1. What is this??](##What is this?)
+ [2. How it works](##How it works)
  + [2.2. How parsers work](####2.2.-How-parsers-work)
  + [2.2. How parsers work](####2.2.-How-parsers-work)
  + [2.3. How to use](####2.3.-How-to-use)
+ [3. How to install](##3.-How-to-install)
+ [4. Notes ](##4.-Notes )


## 1. What is this?

The main idea is to create parsers which can periodically collect new articles
from different sites using API. So, this project is a number of endpoints (Django REST) for parsers that collect data (articles) from the following sites:

+ mel.fm https://mel.fm/
+ habr.com https://habr.com/ru/
+ tinkoff-journal https://journal.tinkoff.ru/


## 2. How it works


#### 2.1. How api works

A parser sequentially collects articles every 20 minutes from all categories which added into database.
For example, for habr.com we can insert into database such categories as programming and math, using django-admin.
Then the parser will collect articles from the main page of the hub dedicated to programming and math and insert into database. 
After that other services and users can get the data using API.
You can see it in the schema:

![](https://github.com/iriskin77/Habr_parser_api/blob/master/images/dj_pars.png)

#### 2.2. How parsers work

All parsers work approximately in the same way. A parser receives a number of links to categories, for example,
math/machine learning for the parser which parses habr.com or school/education for mel-parser. After that the parser
consistently collects articles from each category. You can see it in the schema:

![](https://github.com/iriskin77/Habr_parser_api/blob/master/images/drf_api_parsers.png)

## 2.3. How to use

1) As a superuser you should add categories of a blog into db using Django-admin or POST request.
From these categories parsers will collect data.
For example, it is possible to use for it requests or Postman. 

```python
import requests

url_api: str = "http://127.0.0.1:8000/api/v1/add_mel_category"

data: dict = {"name_cat": "Воспитание", "link_cat": "https://mel.fm/vospitaniye"}

response = requests.post(url=url_api, data=data)

```
If everything is okay, you will receive 201 status. 
it means that your category has been successfully added into db.

2) After that the parser will collect articles which are related to these categories. 
Default crontab is 20 minutes, but you can change it in the project settings:

```python
CELERY_BEAT_SCHEDULE = {
      'pars-data-habr': {
        'task': 'apps.parser_habr.tasks.collect_data_habr',
        'schedule': crontab(minute='*/20'),
    },
    'pars-data-tinkoff': {
        'task': 'apps.parser_mel.tasks.collect_data_mel',
        'schedule': crontab(minute='*/20'),
    },
    'pars-data-mel': {
        'task': 'apps.parser_tink.tasks.collect_data_tinkoff',
        'schedule': crontab(minute='*/20'),
    },
}
```

3) As a superuser you can run parsers manually using the following endpoints:

POST request from the server runs the parsers:

+ http://127.0.0.1:8080/api/v1/pars_habr runs the parser for habr.com
+ http://127.0.0.1:8080/api/v1/pars_mel runs the parser for mel.fm
+ http://127.0.0.1:8080/api/v1/pars_tink runs the parser for tinkoff-journal

If everything is okay you will receive the following answer from the server:
```json
   {
    "Task was created": 200,
    "Task_id": 16,
    "Task_id_celery": "35c467b0-d723-4eea-868d-3e2ed700d622"
   }
```

to GET information about the task you`ve created, use:

+ http://127.0.0.1:8080/api/v1/get_task_info_mel
+ http://127.0.0.1:8080/api/v1/get_task_habr_info
+ http://127.0.0.1:8080/api/v1/get_task_info_tink

```json
   {
    "task_id": 16,
    "celery_task_id": "35c467b0-d723-4eea-868d-3e2ed700d622",
    "task_status": "PENDING",
    "task_result": null
   }
```

to GET parsed articles you can use the following endpoints:

+ http://127.0.0.1:8080/api/v1/articles_habr
+ http://127.0.0.1:8080/api/v1/articles_mel
+ http://127.0.0.1:8080/api/v1/articles_tink

```json
   [
    {
        "id": 1,
        "title": "Размышления о структурном программировании",
        "text": "\nИзначально я хотел назвать статью как нибудь вызывающе, например, \"Как наука может превращаться в религию\..."
        "date": "2023-12-31, 11:53",
        "link": "https://habr.com/ru/articles/784238/",
        "hub": 1,
        "author": 1
    },
    {
        "id": 2,
        "title": "Управление памятью и разделяемыми ресурсами без ошибок",
        "text": "\nМельком пробежал статью Синхронизация операций в .NET на примерах / Хабр, после чего..."
        "date": "2023-12-30, 19:17",
        "link": "https://habr.com/ru/articles/784184/",
        "hub": 1,
        "author": 1
    }
  ]
```

to GET parsed authors of articles you can use the following endpoints:

+ http://127.0.0.1:8080/api/v1/authors_habr
+ http://127.0.0.1:8080/api/v1/authors_mel
+ http://127.0.0.1:8080/api/v1/authors_tink

```json

  [
    {
        "id": 1,
        "author": "rsashka",
        "author_link": "https://habr.com/ru/users/rsashka/"
    },
    {
        "id": 2,
        "author": "nik_vr",
        "author_link": "https://habr.com/ru/users/nik_vr/"
    },
    {
        "id": 3,
        "author": "Litloc",
        "author_link": "https://habr.com/ru/users/Litloc/"
    },
    {
        "id": 4,
        "author": "alextretyak",
        "author_link": "https://habr.com/ru/users/alextretyak/"
    }
  ]  

```

## 3. How to install

You can install it as a docker container:

+ Clone the repo

+ Create .env and fill it:

```python
#django settings

DEBUG = 
SECRET_KEY = 

#smtp server

EMAIL_HOST = 
EMAIL_HOST_USER = 
EMAIL_HOST_PASSWORD = 
EMAIL_PORT = 
EMAIL_USE_TLS = 

# postgres db

NAME =
USER =
PASSWORD =
HOST =
PORT =

```

+ Use the command: <strong>make app</strong>

After that the docker container will be created on the port 8080: http://127.0.0.1:8080

## 4. Notes 

There are things to do:

+ Dockerfile to install the project in a simpler way. <strong>Done</strong>
+ Prometheus for minitoring <strong>Done</strong>
+ Nginx as a proxy server <strong>Done</strong>
+ Maybe deploying the project in a server <strong>In process...</strong>
