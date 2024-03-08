from django.urls import path
from . import views


app_name = 'parser_habr'


urlpatterns = [
    path('pars_habr', views.parse_habr, name='pars_habr'),
    path('get_task_habr_info', views.TaskHabrInfo.as_view(), name='get_task_habr_info'),
    path('list_cats_habr/', views.ListApiHub.as_view(), name='list_cats_habr'),
    path('list_tasks_habr/', views.TaskViewSet.as_view(), name='list_tasks_habr'),
    path('list_articles_habr/', views.TextsViewSet.as_view(), name='list_articles_habr'),
    path('list_authors_habr/', views.AuthorViewSet.as_view(), name='list_authors_habr'),
    path('add_habr_category/', views.AddCategory.as_view(), name='add_habr_category')
]
