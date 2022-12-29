from dataclasses import fields
from rest_framework import serializers
from post.models import Post, Comment, PostImage, CommentImage, PostReport


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'text', 'date',
                  'category', 'tag', 'bump', 'author', 'author_name', 'cover', 'pk']


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['parent','image']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text', 'bump', 'date', 'author', 'author_name', 'image', 'pk']

    def create(self, validated_data):
        parent_id = self.context['parent_id']
        return Comment.objects.create(parent_id=parent_id, **validated_data)


class CommentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentImage
        fields = ['image']

class PostReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReport
        fields = ['postLink', 'type'] 