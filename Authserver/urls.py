"""Authserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token,verify_jwt_token
from rest_framework import routers

from otp.views import obtain_otp_token,verify_otp_token
from rbac.views import obtain_auth_token, RoleViewSet, UserViewSet, MenuViewSet

router = routers.DefaultRouter()
router.register('user',UserViewSet,basename='user')
router.register('role',RoleViewSet,basename='role')
router.register('route',MenuViewSet,basename='route')
urlpatterns = [
    # token
    url(r'^api/token-obtain',obtain_auth_token),
    # jwt
    url(r'^api/jwt-obtain',obtain_jwt_token),
    url(r'^api/jwt-verify',verify_jwt_token),
    # otp
    url(r'^api/otp-obtain',obtain_otp_token),
    url(r'^api/otp-verify',verify_otp_token),

    url(r'', include(router.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
