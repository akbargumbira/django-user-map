# coding=utf-8
"""Model class of custom user for InaSAFE User Map."""
import os
import uuid

from django.contrib.gis.db import models
from django.core.exceptions import ValidationError

from user_map.models.role import Role
from user_map.utilities.utilities import wrap_number
from user_map.app_settings import USER_MODEL


def validate_image(fieldfile_obj):
    """Validate the image uploaded by user.

    :param fieldfile_obj: The object of the file field.
    :type fieldfile_obj: File (django.core.files)
    """
    file_size = fieldfile_obj.file.size
    size_limit_mb = 2.0
    size_limit = size_limit_mb * 1024 * 1024
    if file_size > size_limit:
        raise ValidationError(
            'Maximum image size is %s MB' % size_limit_mb)


def image_path(instance, file_name):
    """Return the proper image path to upload.

    :param file_name: The original file name.
    :type file_name: str
    """
    _, ext = os.path.splitext(file_name)

    file_name = '%s%s' % (uuid.uuid4().hex, ext)
    return os.path.join(
        'user_map',
        'images',
        file_name)


class UserMap(models.Model):
    """User Map class as a OneToOne to AUTH_USER_MODEL."""
    class Meta:
        """Meta class."""
        app_label = 'user_map'

    user = models.OneToOneField(
        USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True)
    location = models.PointField(
        verbose_name='Location',
        help_text='Where are you?',
        srid=4326,
        max_length=255,
        null=False,
        blank=False)
    roles = models.ManyToManyField(
        Role,
        verbose_name='Roles',
        blank=False)
    image = models.ImageField(
        verbose_name='Image',
        help_text='Your photo',
        upload_to=image_path,
        null=False,
        blank=True,
        validators=[validate_image])
    is_hidden = models.BooleanField(
        verbose_name='Hidden Status',
        help_text='Do you wish to hide yourself on the map?',
        default=False)

    def save(self, *args, **kwargs):
        # """Override save method."""
        is_new = not bool(UserMap.objects.filter(pk=self.pk).count())
        if not is_new:
            # Saving a not new object
            usermap = UserMap.objects.get(pk=self.pk)
            # Remove the old image if it's new image
            if usermap.image != self.image:
                usermap.image.delete(save=False)

        # Wrap location data
        self.location.x = wrap_number(self.location.x, [-180, 180])
        self.location.y = wrap_number(self.location.y, [-90, 90])

        super(UserMap, self).save()

    def __str__(self):
        return unicode(self.user).encode('utf-8')
