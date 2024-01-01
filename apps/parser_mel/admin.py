from django.contrib import admin
from .models import Category, Article, Task

# Register your models here.


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'celery_task_id', 'is_success', 'created_at')
    readonly_fields = ('created_at',)
    list_filter = ('is_success',)


@admin.register(Article)
class MelArticlesAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'category', 'date_published')
    list_display_links = ('title',)
    ordering = ('id', 'title', 'category', 'date_published')
    list_per_page = 40
    search_fields = ('title', 'category__name_cat')
    list_filter = ('category__name_cat',)


@admin.register(Category)
class MelCategoriesAdmin(admin.ModelAdmin):

    list_display = ('id', 'name_cat', 'link_cat')
    list_display_links = ('name_cat',)
    ordering = ('id',)
    list_per_page = 40
    search_fields = ('name_cat',)
