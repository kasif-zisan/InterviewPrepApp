from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    parent = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, default="<anon>")
    works_at = models.CharField(max_length=256, blank=True)
    lives = models.CharField(max_length=256, blank=True)
    #birth_date = models.DateField(blank=True, default='2-2-2001')
    gender = models.CharField(max_length=10,
                              choices=[
                                  ('Male', 'Male'),
                                  ('Female', 'Female'),
                                  ('Other', 'Other')
                              ], default='Male')
    avatar = models.ImageField(
        upload_to='user/image', default='user/default.png')
    coverPhoto = models.ImageField(
        upload_to='user/image', default='user/cover.png')


class UserImage(models.Model):
    parent = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='user/image')
