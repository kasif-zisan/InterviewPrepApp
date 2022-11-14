from django.urls import path
from user import views


urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('verify/', views.Verify.as_view(), name='verify'),
    path('login/', views.LogIn.as_view(), name='login'),
    path('logout/', views.LogOut.as_view(), name='logout'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('about/', views.About.as_view(), name='about'),
]
