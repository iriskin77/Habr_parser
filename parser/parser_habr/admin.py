from django.contrib import admin
from .models import Timer, Hub, Texts, Author

# Register your models here.

@admin.register(Texts)
class HabrTextsAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'hub','author', 'date', 'brief_info')
    list_display_links = ('title',)
    ordering = ('id', 'title', 'hub', 'author', 'date')
    list_per_page = 40
    search_fields = ('title', 'author__author', 'hub__hub_name')
    list_filter = ('hub__hub_name',)

    @admin.display(description='Описание')
    def brief_info(self, text: Texts):
        return f'Количество символов: {len(text.text)}'

@admin.register(Author)
class HabrAuthorAdmin(admin.ModelAdmin):

    list_display = ('id', 'author', 'author_link')
    list_display_links = ('author',)
    ordering = ('id',)
    list_per_page = 40
    search_fields = ('author',)


@admin.register(Hub)
class HabrAuthorAdmin(admin.ModelAdmin):

    list_display = ('id', 'hub_name', 'hub_link')
    list_display_links = ('hub_name',)
    ordering = ('id',)
    list_per_page = 40
    search_fields = ('hub_name',)

admin.site.register(Timer)

