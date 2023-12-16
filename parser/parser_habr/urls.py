from django.urls import path
from . import views


urlpatterns = [
    path('parse_habr', views.parse_habr, name='parse_habr'),
]
