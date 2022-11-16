from post.models import Post, Comment
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import PostSerializer, CommentSerializer

class NewPost(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'text', 'author__username']
    ordering_fields = ['bump', 'date']

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['bump', 'date']

    def get_queryset(self):
        return Comment.objects.filter(parent_id=self.kwargs['post_pk'])

    def get_serializer_context(self):
        return {'parent_id': self.kwargs['post_pk']}
