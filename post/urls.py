from django.urls import path
from post import views

urlpatterns = [
    path('newpost/', views.NewPost.as_view(), name='new-post'),
    path('feed/', views.PostAll.as_view(), name='feed'),
    path('details/<int:post_id>/', views.PostDetails.as_view(), name = 'details'),
]
