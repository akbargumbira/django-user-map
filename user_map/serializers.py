# coding=utf-8
"""Serializers for User Map."""
from django.contrib.auth import get_user_model

from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.serializers import ModelSerializer

from user_map.models import UserMap
from user_map.app_settings import API_USER_FIELDS


class UserSerializer(ModelSerializer):
    """User Serializer."""
    class Meta:
        model = get_user_model()
        fields = tuple(field for field in API_USER_FIELDS)


class UserMapSerializer(GeoFeatureModelSerializer):
    """User Map Serializer."""
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserMap
        id_field = False
        geo_field = 'location'
        fields = ('user', 'roles', 'image')
