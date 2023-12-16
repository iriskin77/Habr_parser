from django.db import models

# Create your models here.

class Timer(models.Model):
    """"Таблица для таймера для периода обхода"""""
    minutes = models.IntegerField()

    def __str__(self):
        return str(self.minutes)

    class Meta:
        verbose_name = "Период обхода хабов"
        verbose_name_plural = "Период обхода хабов"

class Hub(models.Model):
    """"Таблица для хабов"""""
    hub_name = models.CharField(max_length=255, verbose_name='Название хаба')
    hub_link = models.URLField(max_length=10000, verbose_name='Ссылка на хаб')

    def __str__(self):
        return self.hub_name

    class Meta:
        verbose_name = "Хабы"
        verbose_name_plural = "Хабы"

class Texts(models.Model):
    """"Таблица для статей с каждого хаба"""""
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
    """"Таблица для авторов"""""
    author = models.CharField(max_length=255, verbose_name='Автор статьи')
    author_link = models.URLField(max_length=10000, verbose_name='Ссылка на автора')

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


