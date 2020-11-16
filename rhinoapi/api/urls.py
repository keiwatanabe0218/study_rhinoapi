from django.urls import path
from django.conf.urls import include

from rest_framework import routers
from .views import ObjectViewSet, UserViewSet, ManageUserView, MoveObjectsViewSet, TwistedTowerViewSet, TwistedTowerView
router = routers.DefaultRouter()
router.register('objects',ObjectViewSet)
router.register('move_objects',MoveObjectsViewSet)
router.register('twisted_tower', TwistedTowerViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('myself/', ManageUserView.as_view(), name='myself'),
    path('',include(router.urls)),
    path('twisted_tower_view/<int:pk>/', TwistedTowerView.as_view(), name='twisted_tower'),
]