# coding=utf-8
"""Views of the apps."""
from exceptions import AttributeError
import json

from django.http import HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView

from rest_framework import generics

from user_map.forms import (
    UserMapForm)
from user_map.models import UserMap, Role
from user_map.app_settings import (
    LEAFLET_TILES, MARKER, FAVICON_FILE, PROJECT_NAME)
from user_map.serializers import UserMapSerializer


class BaseTemplateMixin(object):
    """Mixin for Base Template."""

    @property
    def is_mapped(self):
        """Get status is_mapped of the self.request.user."""
        try:
            # noinspection PyUnresolvedReferences
            is_mapped = bool(self.request.user.usermap)
        except (ObjectDoesNotExist, AttributeError):
            is_mapped = False
        return is_mapped

    def get_context_data(self, **kwargs):
        # noinspection PyUnresolvedReferences
        context = super(BaseTemplateMixin, self).get_context_data(**kwargs)
        context['FAVICON_PATH'] = FAVICON_FILE
        context['PROJECT_NAME'] = PROJECT_NAME
        return context


class IndexView(BaseTemplateMixin, TemplateView):
    """Index page of user map."""
    template_name = 'user_map/index.html'

    @property
    def information_modal(self):
        """Get information modal."""
        return loader.render_to_string(
            'user_map/information_modal.html')

    @property
    def data_privacy(self):
        """Get data privacy content."""
        return loader.render_to_string(
            'user_map/data_privacy.html')

    @property
    def leaflet_tiles(self):
        """Get leaflet tiles for the template."""
        return dict(
            url=LEAFLET_TILES[0][1],
            option=LEAFLET_TILES[0][2]
        )

    @property
    def user_popup(self):
        """Get user popup template."""
        return loader.render_to_string(
            'user_map/user_info_popup_content.html')

    def get_user_menu(self):
        """Get user menu at the left side."""
        return loader.render_to_string(
            'user_map/user_menu_button.html',
            {'user': self.request.user, 'is_mapped': self.is_mapped}
        )

    def get_filter_menu(self):
        """Get filter menu at the right side."""
        roles = Role.objects.all()
        return loader.render_to_string(
            'user_map/filter_menu.html',
            {'roles': roles}
        )

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update(
            {
                'data_privacy_content': self.data_privacy,
                'information_modal': self.information_modal,
                'user_menu_button': self.get_user_menu(),
                'filter_menu': self.get_filter_menu(),
                'leaflet_tiles': json.dumps(self.leaflet_tiles),
                'is_mapped': self.is_mapped,
                'marker': json.dumps(MARKER),
                'user_info_popup_template': self.user_popup,
                'roles': json.dumps(list(Role.objects.all().values()))
            }
        )
        return context


class UserMapList(generics.ListAPIView):
    """List of User Map with REST."""
    queryset = UserMap.objects.filter(is_hidden=False)
    serializer_class = UserMapSerializer


class UserAddView(BaseTemplateMixin, CreateView):
    """View to add user to the map."""
    model = UserMap
    form_class = UserMapForm
    template_name = 'user_map/user_add_update.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.add_message(
            self.request,
            messages.INFO,
            'You have been added successfully to the map!'
        )
        return super(UserAddView, self).form_valid(form)

    def get_success_url(self):
        return reverse('user_map:index')

    def dispatch(self, request, *args, **kwargs):
        if self.is_mapped:
            return HttpResponseRedirect(reverse('user_map:index'))
        return super(UserAddView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserAddView, self).get_context_data(**kwargs)
        context['title'] = 'Add me to the map!'
        context['description'] = ('Hey %s, please provide your information '
                                  'on the form below.') % self.request.user
        return context


class UserUpdateView(BaseTemplateMixin, UpdateView):
    """View to update a user."""
    model = UserMap
    form_class = UserMapForm
    template_name = 'user_map/user_add_update.html'

    def get(self, request, **kwargs):
        try:
            self.object = self.request.user.usermap
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('user_map:index'))

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        return self.request.user.usermap

    def get_success_url(self):
        return reverse('user_map:index')

    def form_valid(self, form):
        # form.instance.user = self.request.user
        messages.add_message(
            self.request,
            messages.INFO,
            'You are successfully updated!'
        )
        return super(UserUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update Profile'
        context['description'] = ('Hey %s, please change the information you '
                                  'want to update below!') % self.request.user
        return context
