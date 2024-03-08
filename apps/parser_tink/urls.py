from django.urls import path
from . import views


app_name = 'parser_tink'


urlpatterns = [
    #path('', include(router.urls)),
    path('pars_tink', views.parse_tink, name='pars_tink'),
    path('get_task_info_tink', views.get_task_info, name='get_task_info_tink'),
    path('add_tink_category', views.add_tink_category, name='add_tink_category'),
    path('list_cats_tinkoff', views.CategoryApiList.as_view(), name='list_cats_tinkoff'),
    path('list_tasks_tinkoff', views.TaskViewSet.as_view(), name='list_tasks_tinkoff'),
    path('list_articles_tinkoff', views.ArticleViewSet.as_view(), name='list_articles_tinkoff'),
    path('list_authors_tinkoff', views.AuthorViewSet.as_view(), name='list_authors_tinkoff')

]
