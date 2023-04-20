from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django.http.response import JsonResponse

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
            return PostModel.objects.filter(user=request.user)
        return PostModel.objects.none()
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class GetAllGistsView(View := __import__("django").views.View):
    def get(self, _):
        response = {"error": True, "message": "Error!"}
        return JsonResponse(response)
    
    def post(self, request):
        response = {"error": True, "message": "Error!"}
        token = request.POST.get("token")
        content = request.POST.get("content")
        success = gist.createGist(token, content)
        if success:
            response = {"error": False, "message": "Success!"}
        return JsonResponse(response)
