from django.contrib import admin
from .models import Post, Tag, Comment, PostImage, CommentImage, PostReport
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(PostImage)
admin.site.register(CommentImage)   
admin.site.register(PostReport) 

