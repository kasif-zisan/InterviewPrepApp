from rest_framework import serializers

from user.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'image', 'date', 'bump', 'author']
