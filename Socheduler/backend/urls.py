from django.urls import path, include
from rest_framework import routers
from .views import PostView, GetAllGistsView

from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()
router.register(r"posts", PostView, basename="post")

urlpatterns = [
    path("", include(router.urls)),
    path("gists/", csrf_exempt(GetAllGistsView.as_view()), name="gists"),
]
