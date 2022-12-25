from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime


class Tag(models.Model):
    tag_name = models.CharField(max_length=256)


class Post(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    bump = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    QUESTIONS = 'questions'
    ENTERTAINMENT = 'entertainment'
    EXPERIENCES = 'experiences'
    category = models.CharField(max_length=20,
                                choices=[
                                    (QUESTIONS, 'questions'),
                                    (ENTERTAINMENT, 'entertainment'),
                                    (EXPERIENCES, 'experiences')
                                ], default=ENTERTAINMENT)
    tag = models.ManyToManyField(
        Tag, related_name='post', blank=True
    )
    cover = models.ImageField(upload_to='post/image',
                              default='post/image/default.jpg')


    def author_name(self):
        obj = User.objects.get(pk=self.author.pk)
        return obj.username
    
    '''def date(self):
        return str(self.date_time).split()[0]
    
    def time(self):
        time = list(str(self.date_time).split()[1].split(':'))
        time[2] = time[2].split('.')[0]
        if int(time[0]) > 12:
            time[0] = str(int(time[0]) - 12)
            time_str = ":".join(each for each in time[:3]) + ' pm'
        else:
            time_str = ":".join(each for each in time[:3]) + ' am'
        
        return time_str'''



class PostImage(models.Model):
    parent = models.ForeignKey(
        Post, on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='post/image')


class Comment(models.Model):
    text = models.TextField()
    bump = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        Post, on_delete=models.CASCADE
    )
    image =  models.ImageField(upload_to='comment/image', blank = True, null = True, default= None)
    def author_name(self):
        obj = User.objects.get(pk=self.author.pk)
        return obj.username

    ''' def date(self):
        return str(self.date_time).split()[0]
    
    def time(self):
        time = list(str(self.date_time).split()[1].split(':'))
        time[2] = time[2].split('.')[0]
        if int(time[0]) > 12:
            time[0] = str(int(time[0]) - 12)
            time_str = ":".join(each for each in time[:3]) + ' pm'
        else:
            time_str = ":".join(each for each in time[:3]) + ' am'
        
        return time_str'''


class CommentImage(models.Model):
    parent = models.ForeignKey(
        Post, on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='comment/image')