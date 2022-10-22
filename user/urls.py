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
    path('newpost/', new_post.as_view(), name='new-post'),
    path('feed/',views.feed, name='feed'),
    path('<int:post_id>/', views.postdetails, name = 'details'),
    path('verify/', views.verify, name='verify')
]
