from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.compat import coreapi, coreschema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.utils import model_meta
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rbac.models import UserProfile, Role, Menu
from rbac.serializers import RoleInfoSerializer, UserProfileSerializer, MenuSerializer, UserUpdateSerializer, \
    RoleUpdateSerializer


class UserViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    @action(methods=['get'], detail=False)
    def getuserinfo(self, request):
        u = request.user
        data = self.get_serializer(u.userprofile, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['put'],detail=True)
    def updateuser(self,request,pk=None):
        o = get_object_or_404(UserProfile,pk=pk)
        data = request.data
        s = UserUpdateSerializer(data=data,instance=o.user)
        if s.is_valid(raise_exception=True):
            o.nickname = data['name']
            s.update(o.user,s.validated_data)
            o.save()
        roles = Role.objects.filter(name__in=data['roles'])
        if roles:
            o.user.role_set.clear()
            o.user.role_set.add(*data['roles'])
        return Response(data=UserProfileSerializer(o).data, status=status.HTTP_200_OK)


class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleInfoSerializer

    @action(methods=['put'], detail=True)
    def updaterole(self, request, pk=None):
        o = get_object_or_404(Role, pk=pk)
        data = request.data
        s = RoleUpdateSerializer(data=data, instance=o)
        if s.is_valid(raise_exception=True):
            s.update(o, s.validated_data)
        print(data['routes'])
        menus = Menu.objects.filter(id__in=data['routes'])
        if menus:
            o.menu_set.clear()
            o.menu_set.add(*data['routes'])
        return Response(data=RoleInfoSerializer(o).data, status=status.HTTP_200_OK)


class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def display(self,o):
        s = self.get_serializer(o)
        data = s.data.copy()
        children = o.children.all()
        if len(children) > 0:
            data['children'] = [self.display(child) for child in children]
        return data

    def list(self, request, *args, **kwargs):
        o = self.queryset.get(pk=1)
        menutree = self.display(o)
        return Response(menutree['children'])


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Username",
                        description="Valid username for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


obtain_auth_token = ObtainAuthToken.as_view()
