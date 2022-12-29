from django.shortcuts import get_object_or_404, render
from .models import UserProfile, UserImage
from .serializers import UserProfileSerializer, UserImageSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from djoser.views import UserViewSet


class UserProfileViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = UserProfile
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            (self.__class__.__name__, lookup_url_kwarg)
        )
        obj = get_object_or_404(
            UserProfile, parent__id=self.kwargs[lookup_url_kwarg])

        return obj


class UserImageViewSet(ModelViewSet):
    serializer_class = UserImageSerializer

    def get_queryset(self):
        queryset = UserImage.objects.all()
        user__id = self.request.query_params.get('user__id')
        if user__id:
            queryset = queryset.filter(user=user__id)
        print(list(queryset))
        return queryset


class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        kwargs['data'] = {"uid": self.kwargs['uid'],
                          "token": self.kwargs['token']}

        return serializer_class(*args, **kwargs)

    def activation(self, request, uid, token, *args, **kwargs):
        super().activation(request, *args, **kwargs)
        return render(request, "user/return.html")


class EndpointList(APIView):
    def get(self, request):
        return Response({
            'authentication': {
                'sign up': 'http://127.0.0.1:8000/auth/users/',
                'activate account': 'http://127.0.0.1:8000/activate/<uid>/<token>/',
                'log in(generate jwt token)': 'http://127.0.0.1:8000/auth/jwt/create',
                'refresh jwt token': 'http://127.0.0.1:8000/auth/jwt/refresh',
                'current user': 'http://127.0.0.1:8000/auth/users/me/'
            },
            'profile api': {
                'profile create': 'http://127.0.0.1:8000/api/user/profile',
                'current user profile': 'http://127.0.0.1:8000/api/user/profile/<user__pk>'
            },
            'post api': {
                'all post/ create': 'http://127.0.0.1:8000/api/post/post/',
                'post retrieve/ update/ delete': 'http://127.0.0.1:8000/api/post/post/<post__pk>',
                'post images/create': 'http://127.0.0.1:8000/api/post/post/<post__pk>/postImage',
                'post image retrieve': 'http://127.0.0.1:8000/media/<path>',

                'all comment/ create': 'http://127.0.0.1:8000/api/post/post/<post__pk>/comment',
                'comment retrieve/ update/ delete': 'http://127.0.0.1:8000/api/post/post/<post__pk>/comment/<comment_pk>',
                'comment images/create': 'http://127.0.0.1:8000/api/comment/<comment__pk>/commentImage',
                'comment image retrieve': 'http://127.0.0.1:8000/media/<path>'
            }})