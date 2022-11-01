from unittest.util import _MAX_LENGTH
from urllib import request
from rest_framework import serializers

from user.models import Post, Comments

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'date', 'bump', 'author']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['text', 'image', 'bump', 'time', 'author', 'parent']

class jsonString(serializers.Serializer):
    text = serializers.CharField(max_length=None, allow_blank=False)