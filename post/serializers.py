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


class StringSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=None, allow_blank=False)


class EditPostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=None)
    text = serializers.CharField(max_length=None)
