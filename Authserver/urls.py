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
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token,verify_jwt_token
from rest_framework.authtoken.views import obtain_auth_token

from otp.views import obtain_otp_token,verify_otp_token
from rbac.views import UserView

urlpatterns = [

    url(r'^user',UserView.as_view()),
    # token
    url(r'^api/token-obtain',obtain_auth_token),
    # jwt
    url(r'^api/jwt-obtain',obtain_jwt_token),
    url(r'^api/jwt-verify',verify_jwt_token),
    # otp
    url(r'^api/otp-obtain',obtain_otp_token),
    url(r'^api/otp-verify',verify_otp_token),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
