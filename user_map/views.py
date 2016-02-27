# coding=utf-8
"""Views of the apps."""
import csv
from exceptions import AttributeError

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View

from rest_framework import generics

from user_map.forms import (
    UserMapForm)
from user_map.models import UserMap, Role
from user_map.app_settings import LEAFLET_TILES, MARKER
from user_map.serializers import UserMapSerializer


class IndexView(View):
    """Index page of user map."""
    def get(self, request):
        information_modal = loader.render_to_string(
            'user_map/information_modal.html')
        data_privacy_content = loader.render_to_string(
            'user_map/data_privacy.html')

        try:
            is_mapped = bool(request.user.usermap)
        except (ObjectDoesNotExist, AttributeError):
            is_mapped = False

        user_menu_button = loader.render_to_string(
            'user_map/user_menu_button.html',
            {'user': request.user, 'is_mapped': is_mapped}
        )

        roles = Role.objects.all()
        filter_menu = loader.render_to_string(
            'user_map/filter_menu.html',
            {'roles': roles}
        )

        leaflet_tiles = dict(
            url=LEAFLET_TILES[0][1],
            attribution=LEAFLET_TILES[0][2]
        )

        context = {
            'data_privacy_content': data_privacy_content,
            'information_modal': information_modal,
            'user_menu_button': user_menu_button,
            'filter_menu': filter_menu,
            'leaflet_tiles': leaflet_tiles,
            'is_mapped': is_mapped,
            'marker': MARKER
        }

        return render(request, 'user_map/index.html', context)


class UserMapList(generics.ListAPIView):
    """List of User Map with REST."""
    queryset = UserMap.objects.filter(is_hidden=False)
    serializer_class = UserMapSerializer


class UserAddView(CreateView):
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
        try:
            is_mapped = bool(request.user.usermap)
        except (ObjectDoesNotExist, AttributeError):
            is_mapped = False

        if is_mapped:
            return HttpResponseRedirect(reverse('user_map:index'))
        return super(UserAddView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserAddView, self).get_context_data(**kwargs)
        context['title'] = 'Add me to the map!'
        context['description'] = ('Hey %s, please provide your information '
                                  'on the form below.') % self.request.user
        return context


class UserUpdateView(UpdateView):
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
