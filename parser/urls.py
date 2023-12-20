"""
URL configuration for parser project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from parser_habr.views import AuthorViewSet, HubViewSet, TextsViewSet
from .swagger import urlpatterns as swagger_urls

router_authors = routers.DefaultRouter()
router_authors.register(r'authors', AuthorViewSet)

router_hubs = routers.DefaultRouter()
router_hubs.register(r'hubs', HubViewSet)

router_texts = routers.DefaultRouter()
router_texts.register(r'texts', TextsViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/', include('parser_habr.urls')),
    path('api/v1/', include(router_authors.urls), name='list_authors'),
    path('api/v1/', include(router_hubs.urls), name='list_hubs'),
    path('api/v1/', include(router_texts.urls), name='list_texts'),
]

urlpatterns += swagger_urls
