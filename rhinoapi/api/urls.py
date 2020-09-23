from django.urls import path
from django.conf.urls import include

from rest_framework import routers
from .views import ObjectViewSet, UserViewSet, ManageUserView
router = routers.DefaultRouter()
router.register('objects',ObjectViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('myself/', ManageUserView.as_view(), name='myself'),
    path('',include(router.urls)),
]