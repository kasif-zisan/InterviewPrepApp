from django.urls import path, include
from user import views
from .views import new_post


urlpatterns = [
    path('',views.home, name="home"),
    path('signup/',views.signUp, name="signup"),
    path('logout/',views.logOut, name='logout'),
    path('login/', views.logIn, name='login'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    #path('newpost/', new_post.as_view(), name='new-post'),
    path('newpost/', views.new_post, name='new-post'),
    path('feed/',views.post_all, name='feed'),
    path('post/<int:post_id>/', views.post_details, name = 'details'),
    path('verify/', views.verify, name='verify')
]
