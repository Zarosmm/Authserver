import base64
import datetime
import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid

fss_share = FileSystemStorage(location=settings.SHARE_DATA)


def save_image(filename, datainbase64):
    imgdata = base64.b64decode(datainbase64)
    return fss_share.save(filename, ContentFile(imgdata))


def generate_picture_path(instance, filename):
    a = filename.split('.')
    ext = a[-1] if len(a) > 1 else 'jpg'
    today = datetime.date.today()
    path = os.path.join(settings.PICTURE_ASSETS_PATH, today.isoformat(), '%s.%s' % (instance.id, ext))
    instance.path = os.path.join(settings.SHARE_DATA, path)
    return instance.path


def generate_default_nickname():
    uid = uuid.uuid4()
    uid_slice = str(uid).split('-')[-1]
    return uid_slice.upper()


@receiver(signal=signals.post_save, sender=User)
def CreateToken(sender, instance, created, **kwargs):
    if created:
        token = Token.objects.create(
            user=instance
        )


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(storage=fss_share, upload_to=generate_picture_path, null=True, verbose_name="图片文件")
    nickname = models.CharField(max_length=256, default=generate_default_nickname, verbose_name="昵称")
    hotpcount = models.IntegerField(default=0, verbose_name="HOTP_KEY_COUNT")
    money = models.FloatField(default=0, verbose_name="余额")
    member = models.BooleanField(default=False, verbose_name="会员")
    viptime = models.DateTimeField(blank=True, null=True, verbose_name="会员到期时间")


class Role(models.Model):
    """
    角色：绑定权限
    """
    name = models.CharField(max_length=32, unique=True, verbose_name="角色名")
    code = models.CharField(max_length=32, blank=True)
    description = models.CharField(max_length=512)
    user = models.ManyToManyField(User, blank=True)

    class Mate:
        verbose_name = "角色表"
        verbose_name_plural = verbose_name


class Menu(models.Model):
    """
    菜单
    """
    title = models.CharField(max_length=32)
    parent = models.ForeignKey("Menu", null=True, related_name='children', blank=True, on_delete=models.CASCADE)
    path = models.CharField(max_length=128, null=True, blank=True)
    icon = models.CharField(max_length=128, null=True)
    index = models.IntegerField(null=True)
    componentPath = models.CharField(max_length=128, null=True, blank=True)
    page = models.BooleanField(default=True)

    role = models.ManyToManyField(Role, blank=True)
