from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet, SocialMediaAccountViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'social-accounts', SocialMediaAccountViewSet, basename='social_account')

urlpatterns = [
    path('', include(router.urls)),
]
