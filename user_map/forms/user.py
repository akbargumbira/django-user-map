from django.contrib.gis import forms
from leaflet.forms.widgets import LeafletWidget

from user_map.models import User, Role


class UserForm(forms.ModelForm):
    """Form for user model."""
    name = forms.CharField(
        label='Your name',
        widget=forms.TextInput)
    email = forms.EmailField(
        label='Your email',
        widget=forms.EmailInput)
    password = forms.CharField(
        label='Your password',
        widget=forms.PasswordInput)
    website = forms.URLField(
        label='Your website',
        widget=forms.URLInput)
    location = forms.PointField(
        label='Click your location on the map',
        widget=LeafletWidget())
    role = forms.ModelChoiceField(
        label='Your role',
        queryset=Role.objects.filter(sort_number__gte=1),
        initial=1)
    email_updates = forms.BooleanField(label='Receive project news and updates')

    class Meta:
        """Association between models and this form."""
        model = User
        fields = ['name', 'email', 'password', 'website', 'role',
                  'email_updates', 'location']

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
