from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp


def get_user_token(request, provider: str | list[str]) -> str | list[dict]:
    try:
        user_account = SocialAccount.objects.get(user=request.user)
        tokens = []
        if isinstance(provider, list):
            for pr in provider:
                sa = SocialApp.objects.get(provider=pr.lower())
                tokens.append(
                    {
                        "token": SocialToken.objects.get(
                            app=sa, account=user_account
                        ).token,
                        "provider": pr,
                    }
                )
            return tokens
        social_app = SocialApp.objects.get(provider=provider.lower())
        token = SocialToken.objects.get(app=social_app, account=user_account).token
        return token
    except SocialAccount.DoesNotExist:
        return []
