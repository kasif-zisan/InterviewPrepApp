from django.contrib import admin
from .models import Post, Tag, Comments, PostImage, CommentImage
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comments)
admin.site.register(PostImage)
admin.site.register(CommentImage)    

