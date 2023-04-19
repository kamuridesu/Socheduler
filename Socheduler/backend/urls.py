from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet, SocialMediaAccountViewSet, GetAllGistsView

from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(
    r"social-accounts", SocialMediaAccountViewSet, basename="social_account"
)

urlpatterns = [
    path("", include(router.urls)),
    path("gists/", csrf_exempt(GetAllGistsView.as_view()), name="gists"),
]
