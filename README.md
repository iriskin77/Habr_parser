## What is this?

The main idea is to create parsers which can collect new articles
from different sites using API. So, this project is an api (Django REST) for parsers that collect data (articles) from the following sites:

+ mel.fm https://mel.fm/
+ habr.com https://habr.com/ru/
+ tinkoff-journal https://journal.tinkoff.ru/


## How it works


#### How api works

A parser sequentially collects articles from all categories which added into database.
For example, for habr.com we can insert into database such categories as programming and math, using django-admin.
Then the parser will collect articles from the main page of the hub dedicated to programming and math and insert into database. 
After that other services can get the data using API. If a service sets a timer, then the parser can do it every 1/2/3 hours/days/weeks. 
You can see it in the schema:

![](https://github.com/iriskin77/Habr_parser_api/blob/master/images/dj_pars.png)

#### How parsers work

All parsers work approximately in the same way. A parser receives a number of links to categories, for example,
math/machine learning for the parser which parses habr.com or school/education for mel-parser. After that the parser
consistently collects articles from each category. You can see it in the schema:

![](https://github.com/iriskin77/Habr_parser_api/blob/master/images/parser.png)

## How to use

1) Add categories of a blog you want to parse into db using POST request. For example, it is possible to use for it
requests or Postman. 

```python
import requests

url_api: str = "http://127.0.0.1:1234/api/v1/add_mel_category"

data: dict = {"name_cat": "Воспитание", "link_cat": "https://mel.fm/vospitaniye"}

response = requests.post(url=url_api, data=data)

```
If everything is okay, you will receive 201 status. 
it means that your category has been successfully added into db.

2) After that you can parse articles which are related to these categories using the following
endpoints:

POST request from the server runs the parsers:

+ http://127.0.0.1:1234/api/v1/pars_habr runs the parser for habr.com
+ http://127.0.0.1:1234/api/v1/pars_mel runs the parser for mel.fm
+ http://127.0.0.1:1234/api/v1/pars_tink runs the parser for tinkoff-journal

If everything is okay you will receive the following answer from the server:
```json
   {
    "Task was created": 200,
    "Task_id": 16,
    "Task_id_celery": "35c467b0-d723-4eea-868d-3e2ed700d622"
   }
```

to GET information about the task you`ve created, use:

+ http://127.0.0.1:1234/api/v1/get_task_info_mel
+ http://127.0.0.1:1234/api/v1/get_task_habr_info
+ http://127.0.0.1:1234/api/v1/get_task_info_tink

```json
   {
    "task_id": 16,
    "celery_task_id": "35c467b0-d723-4eea-868d-3e2ed700d622",
    "task_status": "PENDING",
    "task_result": null
   }
```

to GET parsed articles you can use the following endpoints:

+ http://127.0.0.1:1234/api/v1/articles_habr
+ http://127.0.0.1:1234/api/v1/articles_mel
+ http://127.0.0.1:1234/api/v1/articles_tink

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

+ http://127.0.0.1:1234/api/v1/authors_habr
+ http://127.0.0.1:1234/api/v1/authors_mel
+ http://127.0.0.1:1234/api/v1/authors_tink

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

## How to install

You can install it as a docker container:

+ Clone the repo

+ Use the command: <strong>make app</strong>

After that the docker container will be created on the port 1234: http://127.0.0.1:1234



## Notes 

There are things to do:

+ Dockerfile to install the project in a simpler way. Now it is quit difficult to do... <strong>Done</strong>
+ Maybe deploying the project in a server <strong>It is not done yet...</strong>
