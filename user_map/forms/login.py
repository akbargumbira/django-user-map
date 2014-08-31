# coding=utf-8
"""Django Forms for Login."""
from django import forms


class LoginForm(forms.Form):
    """Form for user to log in."""
    class Meta:
        """Meta of the form."""
        fields = ['email', 'password']

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'john@doe.com',
            })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your s3cr3T password'
            })
    )

