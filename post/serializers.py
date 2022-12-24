from rest_framework import serializers
from post.models import Post, Comment, PostImage, CommentImage


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'text', 'date_time', 'date', 'time',
                  'category', 'tag', 'bump', 'author', 'author_name', 'cover', 'pk']


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['parent','image']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text', 'bump', 'date_time', 'date', 'time', 'author', 'author_name', 'image']

    def create(self, validated_data):
        parent_id = self.context['parent_id']
        return Comment.objects.create(parent_id=parent_id, **validated_data)


class CommentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentImage
        fields = ['image']