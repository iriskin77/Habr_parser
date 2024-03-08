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
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers
#from apps.parser_mel.urls import router as tink_router
#from apps.parser_tink.urls import router as mel_router
#from apps.parser_habr.urls import router as habr_router
#from .swagger import urlpatterns as swagger_urls
from django.conf import settings
from django.conf.urls.static import static
#from .swagger import urlpatterns as doc_urls


router = routers.DefaultRouter()

#router.registry.extend(tink_router.registry)
#router.registry.extend(mel_router.registry)
#router.registry.extend(habr_router.registry)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/', include('apps.parser_habr.urls')),
    path('api/v1/', include('apps.parser_tink.urls')),
    path('api/v1/', include('apps.parser_mel.urls')),
    path('api/v1/', include((router.urls, 'api'), namespace='api')),
    #path('api/v1/', include(swagger_urls)),
    #path(r'api/v1/auth/', include('djoser.urls')),
    #re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('', include('django_prometheus.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs')

]

#urlpatterns += doc_urls




