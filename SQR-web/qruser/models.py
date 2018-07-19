from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth import get_user_model

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class User(AbstractUser):
    secret_word = models.CharField(max_length=16, blank=False)
    school_name = models.CharField(max_length=100)
    school_klass = models.CharField(max_length=2)
    school_klass_litera = models.CharField(max_length=2)

class UserAction(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    is_come_in = models.BooleanField(null=False)

    def __str__(self):
        template = '{0.user} {0.date_time}'
        return template.format(self)