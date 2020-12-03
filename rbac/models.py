from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid


def generate_default_nickname():
    uid = uuid.uuid4()
    uid_slice = str(uid).split('-')[-1]
    return uid_slice.upper()


@receiver(signal=signals.post_save, sender=User)
def CreateToken(sender, instance, created,**kwargs):
    if created:
        token = Token.objects.create(
            user=instance
        )


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nickname = models.CharField(max_length=256,default=generate_default_nickname,verbose_name="昵称")
    hotpcount = models.IntegerField(default=0,verbose_name="HOTP_KEY_COUNT")
    money = models.FloatField(default=0,verbose_name="余额")
    member = models.BooleanField(default=False,verbose_name="会员")
    viptime = models.DateTimeField(blank=True,null=True,verbose_name="会员到期时间")


