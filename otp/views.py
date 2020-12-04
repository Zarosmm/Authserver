from django.conf import settings
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
import datetime
import pyotp
import base64
import hashlib

# 限时
from utils.jwtverify import JWTVerify


def generate_totp(username, interval=10):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")[:-2] + '00'
    time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    salt = hashlib.sha224(bytes(username + 'zarosmm.com' + settings.SECRET_KEY, encoding='utf-8')).digest()
    secretKey = base64.b32encode(salt)
    totp = pyotp.TOTP(secretKey, interval=interval)
    key = totp.at(time)
    # return 'T' + str(key)
    return str(key)


# 不限时
# def generate_hotp(username, count):
#     salt = hashlib.sha224(bytes(username + 'zarosmm.com' + settings.SECRET_KEY, encoding='utf-8')).digest()
#     secretKey = base64.b32encode(salt)
#     hotp = pyotp.HOTP(secretKey)
#     key = hotp.at(count)
#     return 'H' + str(key)


class OTPGenView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        u = request.user
        key = generate_totp(u.username)
        return Response(data={'OTP': key}, status=status.HTTP_200_OK)


class OTPVerifyView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        u = request.user
        data = request.data
        key = data['OTP']
        verify = (key == generate_totp(u.username))

        return Response(data=verify, status=status.HTTP_200_OK)


obtain_otp_token = OTPGenView.as_view()
verify_otp_token = OTPVerifyView.as_view()
