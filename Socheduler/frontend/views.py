from allauth.socialaccount.models import SocialToken, SocialAccount

from django.views import View
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from allauth.socialaccount.views import ConnectionsView
from allauth.account import app_settings as account_settings
from django.urls import reverse, reverse_lazy


@method_decorator(login_required, name='dispatch')
class IndexView(View):
    
    def get(self, request):
        context = {"message": "hello world"}
        user_account = SocialAccount.objects.filter(user=request.user, provider='github').first()
        if user_account:
            token = SocialToken.objects.get(account=user_account)
            print(token)
        print(context)
        return render(request, "index.html", context)


@method_decorator(login_required, name="dispatch")
class ProfileView(ConnectionsView):
    template_name = "profile." + account_settings.TEMPLATE_EXTENSION
    success_url = reverse_lazy("frontend_profile")
