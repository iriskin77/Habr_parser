from django.contrib import admin
from .models import Category, Article, Author, Task

# Register your models here.

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Author)
admin.site.register(Task)
