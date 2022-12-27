from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from post import views

postRouter = routers.SimpleRouter()
postRouter.register('post', views.PostViewSet, basename='post')
commentRouter = routers.NestedSimpleRouter(postRouter, 'post', lookup='post')
commentRouter.register('comment', views.CommentViewSet, basename='comment')
commentImageRouter = routers.NestedSimpleRouter(
    commentRouter, 'comment', lookup='comment')

commentRouter.register(
    'postImage', views.PostImageViewSet, basename='postImage')
commentImageRouter.register(
    'commentImage', views.CommentImageViewSet, basename='commentImage')

urlpatterns = [
    path('', include(postRouter.urls)),
    path('', include(commentRouter.urls)),
    path('', include(commentImageRouter.urls)),
    path('report/', views.ReportPost.as_view(), name="report"),
    path('newpost/', views.NewPost.as_view(), name='new-post'),
]
