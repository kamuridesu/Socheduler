from datetime import datetime, timezone
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import PostModel, TaskModel
from .serializers import PostSerializer
from .tasks import createGist

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
        if request.user.is_authenticated:
            return super().retrieve(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                task = TaskModel.objects.get(post=self.queryset.get(pk=kwargs['pk']))
                task.delete()
            except TaskModel.DoesNotExist:
                pass
            return super().destroy(request, *args, **kwargs)

    def update(self, request: Request, *args, **kwargs):
        if request.user.is_authenticated:
            obj = get_object_or_404(self.queryset, pk=kwargs['pk'])
            obj.scheduled_date = datetime.strptime(request.data.get('scheduled_date'), '%Y-%m-%dT%H:%M')
            obj.content = request.data.get("content")
            obj.save()

            try:
                task = TaskModel.objects.get(post=self.queryset.get(pk=kwargs['pk']))
                task.delete()
            except TaskModel.DoesNotExist:
                pass
            countdown = (obj.scheduled_date - datetime.now()).total_seconds()
            task = createGist.apply_async(args=(obj.pk, obj.token, obj.content), countdown=round(countdown))
            new_task = TaskModel.objects.create(task_id=task.id, post=obj)
            new_task.save()

            return Response(status=status.HTTP_204_NO_CONTENT)
