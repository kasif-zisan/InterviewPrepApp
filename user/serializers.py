from rest_framework import serializers
from django.contrib.auth.models import User
#from user.models import Post, Comments

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        Model = User
        fields = ['username', 'email']


class StringSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=None, allow_blank=False)

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