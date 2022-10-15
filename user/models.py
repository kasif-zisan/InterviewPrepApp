from django.conf import settings
from django.db import models
 
 
class Tag(models.Model):
    tag_name = models.CharField(max_length=256)
 
 
class Post(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    image = models.ImageField(blank=True, upload_to = 'user/images/')
    bump = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    tag = models.ManyToManyField(
        Tag, related_name = 'post', blank=True
    )
 
 
class Comments(models.Model):
    text = models.CharField(max_length=256)
    image = models.ImageField(blank=True)
    bump = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        Post, on_delete=models.CASCADE
    )
    
