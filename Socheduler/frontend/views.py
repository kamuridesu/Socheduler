from allauth.account import app_settings as account_settings
from allauth.socialaccount.views import ConnectionsView
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View

from .networking import schedulePostInBackend


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
        user_account = SocialAccount.objects.get(user=request.user)
        social_app = SocialApp.objects.get(provider=provider.lower())
        token = SocialToken.objects.get(app=social_app, account=user_account).token
        schedulePostInBackend(csfr_token, token=token, username = request.user.username, content=content, platform=provider, date_time=date)
        return redirect("/")


@method_decorator(login_required, name="dispatch")
class ProfileView(ConnectionsView):
    template_name = "profile." + account_settings.TEMPLATE_EXTENSION
    success_url = reverse_lazy("frontend_profile")
