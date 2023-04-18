from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import Post, SocialMediaAccount
from .serializers import PostSerializer, SocialAccontSerializer


class MainViewSet(viewsets.ModelViewSet):
    def list(self, request):
        serialized = self.serializer_class(self.queryset, many=True)
        return Response(serialized.data)
    
    def retrieve(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serialized = self.serializer_class(post)
        return Response(serialized.data)


class SocialMediaAccountViewSet(MainViewSet):
    queryset = SocialMediaAccount.objects.all()
    serializer_class = SocialAccontSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(username=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PostViewSet(MainViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
