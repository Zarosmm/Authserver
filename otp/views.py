import pytz
from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
import datetime
import pyotp
import base64
import hashlib


# 限时
def generate_totp(username, interval=10):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")[:-2] + '00'
    time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    salt = hashlib.sha224(bytes(username + 'zarosmm.com' + settings.SECRET_KEY, encoding='utf-8')).digest()
    secretKey = base64.b32encode(salt)
    totp = pyotp.TOTP(secretKey, interval=interval)
    key = totp.at(time)
    return 'T' + str(key)


# 不限时
def generate_hotp(username,count):
    salt = hashlib.sha224(bytes(username + 'zarosmm.com' + settings.SECRET_KEY, encoding='utf-8')).digest()
    secretKey = base64.b32encode(salt)
    hotp = pyotp.HOTP(secretKey)
    key = hotp.at(count)
    return 'H' + str(key)


class OTPView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        u = request.user
        Tkey = generate_totp(u.username)
        Hkey = generate_hotp(u.username,u.userprofile.hotpcount)
        return Response(data={'TOTP': Tkey,'HOTP':Hkey}, status=status.HTTP_200_OK)

    def post(self, request):
        u = request.user
        data = request.data
        Tkey = data['TOTP']
        Hkey = data['HOTP']
        data = {
            'Tverify': Tkey == generate_totp(u.username),
            'Hverify': Hkey == generate_hotp(u.username, u.userprofile.hotpcount)
        }
        if data['Hverify']:
            u.userprofile.hotpcount += 1
            u.userprofile.save()
        return Response(data=data, status=status.HTTP_200_OK)
