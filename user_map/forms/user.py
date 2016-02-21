# coding=utf-8
"""Django forms for User related routines."""
from django.contrib.gis import forms

from leaflet.forms.widgets import LeafletWidget

from user_map.models import UserMap
from user_map.app_settings import LEAFLET_TILES


class UserMapForm(forms.ModelForm):
    """Form for user model."""
    class Meta:
        """Association between models and this form."""
        model = UserMap
        exclude = ['user']
        widgets = {'location': LeafletWidget(attrs={
            'settings_overrides': {
                'TILES': LEAFLET_TILES
            }
        })}
