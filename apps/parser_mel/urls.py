from django.urls import include, path
from rest_framework import routers

from apps.parser_mel.views import TaskViewSet, AuthorViewSet, ArticleViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r'tasks_mel', TaskViewSet, basename='tasks_mel')
router.register(r'authors_mel', AuthorViewSet, basename='authors_mel')
router.register(r'articles_mel', ArticleViewSet, basename='articles_mel')
router.register(r'category_mel', CategoryViewSet, basename='category_mel')


app_name = 'parser_mel'

urlpatterns = [
    path('', include(router.urls))
]
