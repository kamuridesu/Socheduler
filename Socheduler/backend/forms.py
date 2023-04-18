from django import forms
from django.forms.widgets import CheckboxSelectMultiple

from .models import SocialMediaAccount, PLATFORMS

class SocialMediaAccount(forms.Model):
    platform = forms.MultipleChoiceField(choices=PLATFORMS, widget=CheckboxSelectMultiple)

    class Meta:
        model = SocialMediaAccount
        fields = ["username", "platform"]
