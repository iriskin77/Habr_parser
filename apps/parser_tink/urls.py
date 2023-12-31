from django.urls import include, path
from rest_framework import routers
from apps.parser_tink.views import TaskViewSet, AuthorViewSet, ArticleViewSet, CategoryViewSet, parse_tink, get_task_info

router = routers.DefaultRouter()
router.register(r'tasks_tink', TaskViewSet, basename='tasks_tink')
router.register(r'authors_tink', AuthorViewSet, basename='authors_tink')
router.register(r'articles_tink', ArticleViewSet, basename='articles_tink')
router.register(r'category_tink', CategoryViewSet, basename='category_tink')


app_name = 'parser_tink'

urlpatterns = [
    path('', include(router.urls)),
    path('parse_tink', parse_tink, name='parse_tink'),
    path('get_task_info_tink', get_task_info, name='get_task_info_tink')
]
