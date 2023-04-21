from allauth.account import app_settings as account_settings
from allauth.socialaccount.views import ConnectionsView
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View

from .networking import schedulePostInBackend, getAllScheduledPosts
from .utils import get_user_token


@method_decorator(login_required, name="dispatch")
class IndexView(View):
    def get(self, request):
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
        )

    def post(self, request: HttpRequest):
        csfr_token = request.POST.get("csrfmiddlewaretoken")
        provider = request.POST.get("socialMediaPlatform")
        content = request.POST.get("postContent")
        date = request.POST.get("postDate")
        token = self.get_user_token(request, provider)
        schedulePostInBackend(
            csfr_token,
            token=token,
            username=request.user.username,
            content=content,
            platform=provider,
            date_time=date,
        )
        return redirect("/")


@method_decorator(login_required, name="dispatch")
class PostsView(View):
    def get(self, request):
        user_social_accounts = SocialAccount.objects.filter(user=request.user)
        providers = [account.provider for account in user_social_accounts]
        tokens = get_user_token(request, providers)
        scheduled_posts = getAllScheduledPosts(tokens)
        if scheduled_posts:
            return render(
                request,
                "posts.html",
                context={
                    "posts": scheduled_posts
                }
            )
        return render(
            request,
            "error.html",
            context={
                "message": "Go to profile to add a social account!",
                "title": "NO ACCOUNT LINKED!",
            },
        )


@method_decorator(login_required, name="dispatch")
class ProfileView(ConnectionsView):
    template_name = "profile." + account_settings.TEMPLATE_EXTENSION
    success_url = reverse_lazy("frontend_profile")
