from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import UserModel


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        if request._request.method == "POST":
            return None
        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            return None
        token = token.split(" ")[-1]
        try:
            user = UserModel.objects.get(token=token)
        except UserModel.DoesNotExist:
            raise AuthenticationFailed("Invalid token")
        return (user, token)
