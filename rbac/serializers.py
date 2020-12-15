from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.response import Response

from rbac.models import UserProfile, Role, Menu


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    roles = serializers.SerializerMethodField()
    name = serializers.CharField(source='nickname')

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'name', 'money', 'viptime', 'member', 'roles', 'email']

    def get_roles(self, instance):
        u = instance.user
        roles = [r.name for r in u.role_set.all()]
        return roles

    def create(self, validated_data):
        if User.objects.filter(username=validated_data['user']['username']).exists():
            return Response(data={'msg': "用户名重复"})
        user = User.objects.create(
            username=validated_data['user']['username'],
            password=make_password('changeme'),
            email=validated_data['user']['email']
        )
        validated_data.pop('user')
        userprofile = UserProfile.objects.create(
            user=user,
            **validated_data
        )
        return userprofile


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class MenuSerializer(serializers.ModelSerializer):

    checked = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = '__all__'

    def get_checked(self,instance):
        if instance.parent:
            menu = instance
            return reversed(get_parent_id_list(menu)[:-1])


class MenuTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'title', 'path']


class RoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name', 'code', 'description']


class RoleInfoSerializer(serializers.ModelSerializer):
    routes = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = '__all__'

    def get_routes(self, instance):
        menus = instance.menu_set.all()
        if len(menus) > 0:
            ids = [m.id for m in menus]
            data = self.display(MenuTreeSerializer, instance.menu_set.get(parent_id=None), ids)
        else:
            data = {'id': 0, 'title': '/', 'path': '/', 'children': []}
        return [data]

    def display(self, serializer, o, ids):
        s = serializer(o)
        data = s.data.copy()
        children = o.children.filter(id__in=ids)
        data['disabled'] = True
        if len(children) > 0:
            data['children'] = [self.display(MenuTreeSerializer, child, ids) for child in children]
        return data



def get_parent_id_list(obj):
    ids = []
    if obj.parent:
        ids.append(obj.parent.id)
        ids += get_parent_id_list(obj.parent)
    return ids
