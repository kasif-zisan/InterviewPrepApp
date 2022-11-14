from post.models import Post, Comments
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
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
