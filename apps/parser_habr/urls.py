from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register(r'tasks_habr', views.TaskViewSet, basename='tasks_habr')
router.register(r'authors_habr', views.AuthorViewSet, basename='authors_habr')
router.register(r'articles_habr', views.TextsViewSet, basename='articles_habr')


app_name = 'parser_habr'


urlpatterns = [
    path('', include(router.urls)),
    path('pars_habr', views.parse_habr, name='pars_habr'),
    path('get_task_habr_info', views.get_task_habr_info, name='get_task_habr_info'),
    path('add_habr_category/', views.add_habr_category, name='add_habr_category'),
    path('hubs_habr/', views.ListApiHub.as_view(), name='hubs_habr'),
    path('hub_habr/<int:pk>/', views.ListApiHub.as_view(), name='hub_habr'),
]
