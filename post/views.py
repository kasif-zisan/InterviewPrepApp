from post.models import Post, Comment
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from .serializers import PostSerializer, CommentSerializer

class NewPost(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(parent_id=self.kwargs['post_pk'])

    def get_serializer_context(self):
        return {'parent_id': self.kwargs['post_pk']}
