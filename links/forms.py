from django import forms
from django.contrib.auth.models import User


# Registration Form
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "password"]


# Dashboard Link Form (4 URLs)
class LinkForm(forms.Form):
    title1 = forms.CharField(label="Title 1", required=False)
    url1 = forms.URLField(label="URL 1", required=False)

    title2 = forms.CharField(label="Title 2", required=False)
    url2 = forms.URLField(label="URL 2", required=False)

    title3 = forms.CharField(label="Title 3", required=False)
    url3 = forms.URLField(label="URL 3", required=False)

    title4 = forms.CharField(label="Title 4", required=False)
    url4 = forms.URLField(label="URL 4", required=False)