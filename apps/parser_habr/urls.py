from django.urls import path
from . import views
from django.urls import include, path
from rest_framework import routers
from apps.parser_habr.views import TaskViewSet, AuthorViewSet, TextsViewSet, HubViewSet


router = routers.DefaultRouter()

router.register(r'tasks_habr', TaskViewSet, basename='tasks_habr')
router.register(r'authors_habr', AuthorViewSet, basename='authors_habr')
router.register(r'articles_habr', TextsViewSet, basename='articles_habr')
router.register(r'hub_habr', HubViewSet, basename='hub_habr')


app_name = 'parser_habr'

urlpatterns = [
    path('', include(router.urls)),
    path('parse_habr', views.parse_habr, name='parse_habr'),
    path('get_task_info_habr', views.get_task_info, name='get_task_info_habr')
]
