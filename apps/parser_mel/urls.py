from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'tasks_mel', views.TaskViewSet, basename='tasks_mel')
router.register(r'articles_mel', views.ArticleViewSet, basename='articles_mel')


app_name = 'parser_mel'


urlpatterns = [
    path('', include(router.urls)),
    path('pars_mel', views.parse_mel, name='pars_mel'),
    path('get_task_info_mel', views.get_task_info_mel, name='get_task_info_mel'),
    path('add_mel_category', views.add_mel_category, name='add_mel_category'),
    path('cats_mel', views.CategoryApiList.as_view(), name='cats_mel'),
    path('cat_mel/<int:pk>', views.CategoryApiList.as_view())
]
