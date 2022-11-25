from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, default="<Zar>")
    works_at = models.CharField(max_length=256)


class UserImage(models.Model):
    parent = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='user/image')
