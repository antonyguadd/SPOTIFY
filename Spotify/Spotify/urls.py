"""
URL configuration for Spotify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from Api.views import CreateUserView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuración del esquema de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Spotify API",
        default_version='v1',
        description="Documentación de la API de Spotify",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@spotify.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('spotify/', include('Api.urls')),
    path('register/', CreateUserView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Rutas para Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='swagger-json'),
]
