# coding=utf-8
from django import forms


class LoginForm(forms.Form):
    """Form for user to log in."""
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        """Association between model and this form."""
        fields = ['email', 'password']
