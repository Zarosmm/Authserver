from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rbac.models import UserProfile


class UserView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        if User.objects.filter(username=data['username']).exists():
            return Response(data={'msg':"用户名重复"})
        user = User.objects.create(
            username=data['username'],
            password=make_password(data['password']),
            email=data['email']
        )
        userprofile = UserProfile.objects.create(
            user=user,
        )
        if data.get('nickname',None):
            userprofile.nickname = data['nickname']
        userprofile.save()
        print(userprofile.nickname)
        return Response(status=status.HTTP_201_CREATED)

