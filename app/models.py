import time

from django.db import models
from django.contrib.auth.models  import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models


class Invoice(models.Model):
    slug = models.IntegerField(default=int(time.time()))
    download_url = models.CharField(max_length=255, default="")
    file_name = models.CharField(max_length=255, default="")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    digitized = models.BooleanField(default=False)

class AddParsedInfo(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=255, default=str(int(time.time())))
    from_add  = models.CharField(max_length=255, default="")
    to = models.CharField(max_length=255, default="")
    date = models.CharField(max_length=255, default="")
    items = models.CharField(max_length=255, default="")

class UserAddInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=255, default='')
    active = models.BooleanField(default=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserAddInfo.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.useraddinfo.save()
