from django.urls import path, include
from user import views

urlpatterns = [
    path('',views.home, name="home"),
    path('signup/',views.signUp, name="signup"),
    path('logout/',views.logOut, name='logout'),
    path('login/', views.logIn, name='login'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('newpost/', views.new_post, name='new-post')
]
