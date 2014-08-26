# coding=utf-8
from django import forms
from user_map.models import User, Role


class RegistrationForm(forms.ModelForm):
    """Form for user registration."""
    name = forms.CharField(widget=forms.TextInput)
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    website = forms.URLField(widget=forms.URLInput)
    location = forms.CharField(widget=forms.HiddenInput())
    role = forms.ModelChoiceField(queryset=Role.objects.all(), initial=1)
    email_updates = forms.BooleanField(label='Receive project news and updates')

    class Meta:
        """Association between model and this form."""
        model = User
        fields = ['name', 'email', 'password', 'website', 'role',
                  'email_updates']

    def save(self, commit=True):
        """Save form."""
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


