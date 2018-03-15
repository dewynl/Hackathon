from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=15, min_length=5, widget={})
    password = forms.CharField(widget=forms.PasswordInput())
