from rest_framework import serializers
from user.models import Post, Comments


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


class LogInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=None)
    password = serializers.CharField(max_length=None)


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=None)
    name = serializers.CharField(max_length=None)
    email = serializers.CharField(max_length=None)
    worksAt = serializers.CharField(max_length=None)
    password = serializers.CharField(max_length=None)
    passwordConfirm = serializers.CharField(max_length=None)