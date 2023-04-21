from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.http.response import JsonResponse
from rest_framework import status

from .models import PostModel
from .serializers import PostSerializer

from . import gist
from . import auth


class PostView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = PostModel.objects.all()
    authentication_classes = [auth.CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            posts = PostModel.objects.filter(user=request.user)
            serialized = PostSerializer(posts, many=True)
            return Response(serialized.data)
        return Response([])

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]
