from rest_framework import serializers
from post.models import Post, Comments

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'text', 'date', 'bump', 'author']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['text', 'bump', 'time', 'author', 'parent']

