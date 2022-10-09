from django.urls import path, include
from user import views

urlpatterns = [
    path('',views.firstPage, name="firstPage"),
    path('profile/', views.profile, name='profile')
]
