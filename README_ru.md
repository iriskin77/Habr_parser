
Оглавление

+ [1. Что это?](#title1)
+ [2 Как это работает](#title2)
  + [2.1. Как работает API](#title3)
  + [2.2. Как парсеры работают](#title4)
  + [2.3. Как этим пользоваться](#title5)
+ [3. Как установить](#title6)
+ [4. Заметки](#title7)


## <a id="title1">1. Что это ?</a>

Какой-то контент

Основная идея - это создать набор парсеров, которые могут периодически собирать новые статьи
с разных сайтов, используя API. Этот проект представляет собой API (Django REST) для парсеров, которые собирают данные (статьи) со следующих сайтов:

+ mel.fm https://mel.fm/
+ habr.com https://habr.com/ru/
+ tinkoff-journal https://journal.tinkoff.ru/


+ Python (3.11);
+ Django (Wev Framework);
+ PostgreSQL (database);
+ Redis (message broker for celery);
+ Celery (background tasks);
+ Flower (tracking background tasks);
+ logging (logging);
+ Promtheus (monitoring, metrics);
+ Docker and Docker Compose (containerization);
+ Gunicorn (WSGI HTTP Server);
+ Nginx (Web Server).


## <a id="title2">2. Как это работает?</a>

#### <a id="title3">2.1. Как работает API</a>
Каждый парсер периодически последовательно собирает статьи для каждой категории, которая добалвена в БД.
Например, для сайта habr.com можно добавить категории "программирование" и "математика" при помощи панели администратора Django. 
После этого парсер сначала соберет все статьи с главной страницы категории "программирование", потом все статьи с главной страницы
категории "математика", потом добавит их в БД. После этого другие сервисы могут обращаться к этим данным, используя API. 
Визуально это выглядит слеудющим образом:

![](https://github.com/iriskin77/Habr_parser_api/blob/master/images/dj_pars.png)

#### <a id="title4">2.2. Как парсеры работают</a>
Все парсеры работают почти одинаково. Парсер получает набор ссылок на категории из БД. Например, категории "математика" или
"машинное обучение" для парсера, который парсит habr.com, или школа/образование для парсера, который парсит mel.fm.
После этого парсер последовательно обходит каждую категорию и собирает статьи. Визуально это выглядит следующим образом:

![](https://github.com/iriskin77/Habr_parser_api/blob/master/images/drf_api_parsers.png)

#### <a id="title5">2.3. Как этим пользоваться</a>
Прежде всего необходимо добавить в БД ссылки и названия категорий, 
к которым относятся статьи, которые требуется спарсить. Это можно сделать либо
через панель администратора Django, либо использовать POST запрос. 
Это можно сделать с помощью Python или Postman:

```python
import requests

url_api: str = "http://127.0.0.1:8080/api/v1/add_mel_category"

data: dict = {"name_cat": "Воспитание", "link_cat": "https://mel.fm/vospitaniye"}

response = requests.post(url=url_api, data=data)

```

Если все прошло успешно, статус ответа будет 201, что означает, что новый объект в БД
создан.

2) После этого будут парситься, которые относятся к добавленным категориям. Запускаться 
парсеры будут автоматически раз в 20 минут.

3) Однако в качестве администратора (superuser) можно запускать парсеры
самостоятельно с помощью следующих POST запросов.

+ api/v1/pars_habr запускает парсер для сайта habr.com
+ api/v1/pars_mel запускает парсер для сайта  mel.fm
+ api/v1/pars_tink запускает парсер для сайта tinkoff-journal

Если все прошло успешно, будет получен ответ со статусом 200, а также
id (Task_id) сформированной задачи в БД и в Celery (Task_id_celery):

```json
   {
    "Task was created": 200,
    "Task_id": 16,
    "Task_id_celery": "35c467b0-d723-4eea-868d-3e2ed700d622"
   }
```

Чтобы получить информацию о созданной задаче, можно использовать следующие 
GET запросы:

+ http://127.0.0.1:8080/api/v1/get_task_info_mel
+ http://127.0.0.1:8080/api/v1/get_task_habr_info
+ http://127.0.0.1:8080/api/v1/get_task_info_tink

Если все прошло успешно, вы получите следующий ответ:

```json
   {
    "task_id": 16,
    "celery_task_id": "35c467b0-d723-4eea-868d-3e2ed700d622",
    "task_status": "PENDING",
    "task_result": null
   }
```

Когда парсинг закончен и статьи добавлены в БД, вы можете просмотреть их, используя
следующие GET запросы:

+ http://127.0.0.1:8080/api/v1/articles_habr
+ http://127.0.0.1:8080/api/v1/articles_mel
+ http://127.0.0.1:8080/api/v1/articles_tink

Ответ:

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

Кроме того, можно получить информацию об авторах статей:

 http://127.0.0.1:8080/api/v1/authors_habr
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


## <a id="title6">3. Как установить</a>
1) Клонировать репозиторий
2) Создать и заполнить .env файл
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
3) Использовать команду make app

После этого будет создать docker контейнер на порту

## <a id="title7">4. Заметки</a>
Возможные улучшения

+ Добавить Docker, чтобы было возможно установить проект более простым способом.<strong>Сделано</strong>
+ Возможно разворачивание проекта на сервере...
