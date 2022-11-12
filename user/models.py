from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
 
class Tag(models.Model):
    tag_name = models.CharField(max_length=256)
 
 
class Post(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    bump = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    '''tag = models.ManyToManyField(
        Tag, related_name = 'post', blank=True
    )'''


class PostImage(models.Model):
    parent = models.ForeignKey(
        Post, on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='post/image')


class Comments(models.Model):
    text = models.CharField(max_length=256)
    bump = models.IntegerField()
    time = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        Post, on_delete=models.CASCADE
    )


class CommentImage(models.Model):
    parent = models.ForeignKey(
        Post, on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='comment/image')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    name = models.CharField(max_length=256, default="<anon>")
    works_at = models.CharField(max_length=256)


class UserImage(models.Model):
    parent = models.ForeignKey(
        Post, on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='user/image')
    
