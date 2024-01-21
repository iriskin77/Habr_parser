from django.db import models

# Create your models here.

class Task(models.Model):
    """"Celery task table"""""
    celery_task_id = models.CharField(max_length=1001, verbose_name='id celery')
    is_success = models.BooleanField(default=False, verbose_name='Статус задачи')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.celery_task_id

    class Meta:
        verbose_name = "Задачи"
        verbose_name_plural = "Задачи"


class Hub(models.Model):
    """"Hubs table"""""
    hub_name = models.CharField(max_length=255, unique=True, verbose_name='Название хаба')
    hub_link = models.URLField(max_length=10000, unique=True, verbose_name='Ссылка на хаб')

    def __str__(self):
        return self.hub_name

    class Meta:
        verbose_name = "Хабы"
        verbose_name_plural = "Хабы"

class Texts(models.Model):
    """"Texts table from every Hub"""""
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, verbose_name='Название хаба')
    author = models.ForeignKey("Author", on_delete=models.CASCADE, verbose_name='Автор статьи')
    title = models.CharField(max_length=10000, verbose_name='Заголовок')
    text = models.TextField()
    date = models.CharField(max_length=255, verbose_name='Дата публикации на Habr')
    link = models.URLField(max_length=10000)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"


class Author(models.Model):
    """"Authors table"""""
    author = models.CharField(max_length=255, verbose_name='Автор статьи')
    author_link = models.URLField(max_length=10000, verbose_name='Ссылка на автора')

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
