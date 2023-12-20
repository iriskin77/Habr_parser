from django.urls import path
from . import views


urlpatterns = [
    path('parse_habr', views.parse_habr, name='parse_habr'),
    path('get_task_info', views.get_task_info, name='get_task_info')
]
