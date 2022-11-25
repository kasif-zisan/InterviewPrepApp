from rest_framework import serializers
from post.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'text', 'date',
                  'category', 'tag', 'bump', 'author', 'pk']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text', 'bump', 'time', 'author']

    def create(self, validated_data):
        parent_id = self.context['parent_id']
        return Comment.objects.create(parent_id=parent_id, **validated_data)
