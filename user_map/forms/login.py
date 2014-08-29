# coding=utf-8
from django import forms


class LoginForm(forms.Form):
    """Form for user to log in."""
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

    class Meta:
        """Association between models and this form."""
        fields = ['email', 'password']
