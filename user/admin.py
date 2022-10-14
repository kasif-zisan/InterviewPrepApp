from django.contrib import admin
from .models import Tag, Post, Comments

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comments)
