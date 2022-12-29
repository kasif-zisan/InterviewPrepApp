from post.models import Post, Comment, PostImage, CommentImage, PostReport
from post.serializers import PostSerializer, CommentSerializer, PostImageSerializer, CommentImageSerializer, PostReportSerializer
from post.pagination import Pagination
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

class NewPost(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class ReportPost(ListCreateAPIView):
    queryset = PostReport.objects.all()
    serializer_class = PostReportSerializer
    #permission_classes = [IsAuthenticated]


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'text', 'author__username']
    ordering_fields = ['bump', 'date']
    pagination_class = Pagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.all()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset


class PostImageViewSet(ModelViewSet):
    serializer_class = PostImageSerializer
    #permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (FormParser, MultiPartParser, JSONParser)

    def get_queryset(self):
        return PostImage.objects.filter(parent_id=self.kwargs['post_pk'])


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['bump', 'date']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(parent_id=self.kwargs['post_pk'])

    def get_serializer_context(self):
        return {'parent_id': self.kwargs['post_pk']}


class CommentImageViewSet(ModelViewSet):
    serializer_class = CommentImageSerializer
    #permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return CommentImage.objects.filter(parent_id=self.kwargs['comment_pk'])
