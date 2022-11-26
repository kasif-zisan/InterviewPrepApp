from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from user import views
from .views import ActivateUser, EndpointList

router = routers.SimpleRouter()
router.register('profile', views.UserProfileViewSet, basename='profile')

urlpatterns = [
    path('api/user/', include(router.urls)),
    path('activate/<uid>/<token>',
         ActivateUser.as_view({'get': 'activation'}), name='activation'),
    path('', EndpointList.as_view(), name='if youre reading this then youre gay')
]
