from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'tasks_tink', views.TaskViewSet, basename='tasks_tink')
router.register(r'authors_tink', views.AuthorViewSet, basename='authors_tink')
router.register(r'articles_tink', views.ArticleViewSet, basename='articles_tink')


app_name = 'parser_tink'


urlpatterns = [
    path('', include(router.urls)),
    path('pars_tink', views.parse_tink, name='pars_tink'),
    path('get_task_info_tink', views.get_task_info, name='get_task_info_tink'),
    path('add_tink_category', views.add_tink_category, name='add_tink_category'),
    path('cats_tinkoff', views.CategoryApiList.as_view(), name='cat_tink_list'),
    path('cats_tinkoff/<int:pk>', views.CategoryApiList.as_view(), name='cat_tink_list')
]
