from django.contrib import admin
from .models import Tag, Post, Comments, UserProfile

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comments)
admin.site.register(UserProfile)
