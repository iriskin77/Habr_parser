from django.urls import path
from . import views

app_name = 'parser_mel'


urlpatterns = [
    path('pars_mel', views.parse_mel, name='pars_mel'),
    path('get_task_info_mel', views.TaskMelInfo.as_view(), name='get_task_info_mel'),
    path('add_mel_category', views.CategoryApiList.as_view(), name='add_mel_category'),
    path('list_cats_mel', views.CategoryApiList.as_view(), name='list_cats_mel'),
    path('list_tasks_mel', views.TaskViewSet.as_view(), name='list_tasks_mel'),
    path('list_articles_mel', views.ArticleViewSet.as_view(), name='list_articles_mel'),
]
