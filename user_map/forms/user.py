# coding=utf-8
"""Django forms for User related routines."""
from django.contrib.gis import forms
from django.contrib.auth.forms import (
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm)
from leaflet.forms.widgets import LeafletWidget

from user_map.models import User, Role


class UserForm(forms.ModelForm):
    """Form for user model."""
    name = forms.CharField(
        required=True,
        label='Your name',
        widget=forms.TextInput(
            attrs={'placeholder': 'John Doe'})
    )
    email = forms.EmailField(
        required=True,
        label='Your email',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'john@doe.com'})
    )
    password = forms.CharField(
        required=True,
        label='Your password',
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        required=True,
        label='Your password (again)',
        widget=forms.PasswordInput()
    )
    website = forms.URLField(
        required=False,
        label='Your website',
        widget=forms.URLInput(
            attrs={'placeholder': 'http://john.doe.com'})
    )
    location = forms.PointField(
        label='Click your location on the map',
        widget=LeafletWidget())
    role = forms.ModelChoiceField(
        label='Your role',
        queryset=Role.objects.filter(sort_number__gte=1),
        initial=1)
    email_updates = forms.BooleanField(
        required=False,
        label='Receive project news and updates')

    class Meta:
        """Association between models and this form."""
        model = User
        fields = ['name', 'email', 'password', 'password2', 'website', 'role',
                  'location', 'email_updates']

    def clean(self):
        """Verifies that the values entered into the password fields match."""
        cleaned_data = super(UserForm, self).clean()
        if 'password' in cleaned_data and 'password2' in cleaned_data:
            if cleaned_data['password'] != cleaned_data['password2']:
                raise forms.ValidationError(
                    "Passwords don't match. Please enter both fields again.")
        return cleaned_data

    def save(self, commit=True):
        """Save form.

        :param commit: Whether committed to db or not.
        :type commit: bool
        """
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class BasicInformationForm(forms.ModelForm):
    """Form for Basic Information model."""
    name = forms.CharField(
        required=True,
        label='Your name',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'John Doe'})
    )
    email = forms.EmailField(
        required=True,
        label='Your email',
        widget=forms.EmailInput(
            attrs={
                'readonly': 'readonly',
                'placeholder': 'john@doe.com'})
    )
    website = forms.URLField(
        required=False,
        label='Your website',
        widget=forms.URLInput(
            attrs={
                'placeholder': 'http://john.doe.com'})
    )
    role = forms.ModelChoiceField(
        label='Your role',
        queryset=Role.objects.filter(sort_number__gte=1),
        initial=1)
    email_updates = forms.BooleanField(
        required=False,
        label='Receive project news and updates')
    location = forms.PointField(
        label='Click your location on the map',
        widget=LeafletWidget())

    class Meta:
        """Association between models and this form."""
        model = User
        fields = ['name', 'email', 'website', 'role', 'location',
                  'email_updates']

    def save(self, commit=True):
        """Save form.

        :param commit: Whether committed to db or not.
        :type commit: bool
        """
        user = super(BasicInformationForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class CustomSetPasswordForm(SetPasswordForm):
    """Form for password change without using old password field."""
    new_password1 = forms.CharField(
        required=True,
        label='New password',
        widget=forms.PasswordInput())
    new_password2 = forms.CharField(
        required=True,
        label='New password (again)',
        widget=forms.PasswordInput())

    class Meta:
        """Association between models and this form."""
        model = User


class CustomPasswordResetForm(PasswordResetForm):
    """Form for password reset containing email input."""
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'john@doe.com'})
    )

    class Meta:
        """Association between models and this form."""
        model = User
