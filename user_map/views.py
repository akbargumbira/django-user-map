# coding=utf-8
"""Views of the apps."""
import csv
from exceptions import AttributeError

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View

from rest_framework import generics

from user_map.forms import (
    UserMapForm)
from user_map.models import UserMap
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

        leaflet_tiles = dict(
            url=LEAFLET_TILES[0][1],
            attribution=LEAFLET_TILES[0][2]
        )

        context = {
            'data_privacy_content': data_privacy_content,
            'information_modal': information_modal,
            'user_menu_button': user_menu_button,
            'leaflet_tiles': leaflet_tiles,
            'is_mapped': is_mapped,
            'marker': MARKER
        }

        return render(request, 'user_map/index.html', context)


class UserMapList(generics.ListAPIView):
    """List of User Map with Rest Framework.

    ### Operations
    * GET : List all the User Map
    """
    queryset = UserMap.objects.filter(is_hidden=False)
    serializer_class = UserMapSerializer


class UserAddView(CreateView):
    """View to add user to the map."""
    model = UserMap
    form_class = UserMapForm
    template_name = 'user_map/add_user.html'
    # success_url = reverse('user_map:index')

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


@login_required(login_url='user_map:login')
def update_user(request):
    """Update user view.

    :param request: A django request object.
    :type request: request
    """
    anchor_id = '#basic-information'
    if request.method == 'POST':
        if 'change_basic_info' in request.POST:
            anchor_id = '#basic-information'
            basic_info_form = BasicInformationForm(
                data=request.POST, instance=request.user)
            change_password_form = PasswordChangeForm(user=request.user)
            if basic_info_form.is_valid():
                user = basic_info_form.save()
                messages.success(
                    request, 'You have successfully changed your information!')
                return HttpResponseRedirect(
                    reverse('user_map:update_user') + anchor_id)
            else:
                anchor_id = '#basic-information'
        elif 'change_password' in request.POST:
            anchor_id = '#security'
            change_password_form = PasswordChangeForm(
                data=request.POST, user=request.user)
            basic_info_form = BasicInformationForm(instance=request.user)
            if change_password_form.is_valid():
                user = change_password_form.save()
                messages.success(
                    request, 'You have successfully changed your password!')
                return HttpResponseRedirect(
                    reverse('user_map:update_user') + anchor_id)
            else:
                anchor_id = '#security'
    else:
        basic_info_form = BasicInformationForm(instance=request.user)
        change_password_form = PasswordChangeForm(user=request.user)

    return render_to_response(
        'user_map/account/edit_user.html',
        {
            'basic_info_form': basic_info_form,
            'change_password_form': change_password_form,
            'anchor_id': anchor_id,
        },
        context_instance=RequestContext(request)
    )


def download(request):
    """The view to download users data as CSV.

    :param request: A django request object.
    :type request: request

    :return: A CSV file.
    :type: HttpResponse
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    users = User.objects.filter(role__sort_number__gte=1)
    writer = csv.writer(response)

    fields = ['name', 'website', 'role', 'location']
    headers = ['No.']
    for field in fields:
        verbose_name_field = users.model._meta.get_field(field).verbose_name
        headers.append(verbose_name_field)
    writer.writerow(headers)

    for idx, user in enumerate(users):
        row = [idx + 1]
        for field in fields:
            field_value = getattr(user, field)
            row.append(field_value)
        writer.writerow(row)

    return response
