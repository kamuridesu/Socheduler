from allauth.account import app_settings as account_settings
from allauth.socialaccount.views import ConnectionsView
from allauth.socialaccount.models import SocialAccount

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View

from .networking import schedulePostInBackend, getAllScheduledPosts, deleteScheduledPost, getScheduledPost
from .utils import get_user_token


@method_decorator(login_required, name="dispatch")
class IndexView(View):
    def get(self, request: HttpRequest):
        user_social_accounts = SocialAccount.objects.filter(user=request.user)
        if user_social_accounts:
            return render(
                request,
                "index.html",
                context={
                    "platforms": [
                        account.provider.capitalize()
                        for account in user_social_accounts
                    ]
                },
            )
        return render(
            request,
            "error.html",
            context={
                "message": "Go to profile to add a social account!",
                "title": "NO ACCOUNT LINKED!",
            },
            status=401,
        )

    def post(self, request: HttpRequest):
        csfr_token = request.POST.get("csrfmiddlewaretoken")
        provider = request.POST.get("socialMediaPlatform")
        content = request.POST.get("postContent")
        date = request.POST.get("postDate")
        token = get_user_token(request, provider)
        schedulePostInBackend(
            csfr_token,
            uuid=request.user.pk,
            token=token,
            username=request.user.username,
            content=content,
            provider=provider,
            date_time=date,
        )
        return redirect("/")


@method_decorator(login_required, name="dispatch")
class PostsView(View):
    def get(self, request):
        scheduled_posts = getAllScheduledPosts(uuid=request.user.pk)
        if scheduled_posts:
            return render(request, "posts.html", context={"posts": scheduled_posts})
        return render(
            request,
            "error.html",
            context={
                "message": "Please, create a post!",
                "title": "NO POSTS FOUND!",
            },
            status=404,
        )


@method_decorator(login_required, name="dispatch")
class DeletePostsView(View):
    def get(self, request, pk):
        post_id = pk
        if request.GET.get("confirm") == "true":
            is_deleted = deleteScheduledPost(post_id, uuid=request.user.pk)
            if is_deleted:
                return render(request, "delete.html", context={"deleted": True})
            return render(
                request,
                "error.html",
                context={
                    "message": "Please, select a valid post!",
                    "title": "POST NOT FOUND!",
                },
                status=404,
            )
        return render(
            request,
            "delete.html",
        )


@method_decorator(login_required, name="dispatch")
class EditPostsView(View):
    def get(self, request, pk):
        scheduled_post = getScheduledPost(pk, uuid=request.user.pk)
        if scheduled_post:
            return render(
                request,
                "edit.html",
                context={
                    "post": scheduled_post
                },
            )
        return render(
            request,
            "error.html",
            context={
                "message": "Please, create a post!",
                "title": "NO POSTS FOUND!",
            },
            status=404,
        )


@method_decorator(login_required, name="dispatch")
class ProfileView(ConnectionsView):
    template_name = "profile." + account_settings.TEMPLATE_EXTENSION
    success_url = reverse_lazy("frontend_profile")
