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

class Category(models.Model):
    name_cat = models.CharField(max_length=255, verbose_name="Категория")
    link_cat = models.URLField(max_length=10000, verbose_name="Ссылка на категорию")

    def __str__(self):
        return self.name_cat

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Author(models.Model):
    author = models.CharField(max_length=255, default=None, verbose_name="Авторы")
    author_link = models.URLField(max_length=10000, verbose_name='Ссылка на автора')

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = "Авторы"
        verbose_name_plural = "Авторы"

class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    body = models.TextField(verbose_name="Содержание статьи")
    date_published = models.CharField(max_length=255, verbose_name="Дата публикации")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    link = models.URLField(max_length=10000, verbose_name="Ссылка на статью")
    author = models.ForeignKey(Author, on_delete=models.PROTECT, verbose_name="Автор")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статьи"
        verbose_name_plural = "Статьи"
