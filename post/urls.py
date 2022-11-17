from django.urls import path
from django.urls.conf import include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from post import views

postRouter = routers.SimpleRouter()
postRouter.register('post', views.PostViewSet)
commentRouter = routers.NestedSimpleRouter(postRouter, 'post', lookup='post')
commentRouter.register('comment', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(postRouter.urls)),
    path('', include(commentRouter.urls)),
    path('newpost/', views.NewPost.as_view(), name='new-post'),
]
