from django.urls import path, include
from rest_framework import routers
from .views import PostView

from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()
router.register(r"posts", PostView, basename="post")

urlpatterns = [path("", include(router.urls))]
