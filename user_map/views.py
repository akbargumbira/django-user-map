# coding=utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth import (
    login as django_login,
    authenticate,
    logout as django_logout)

from user_map.forms import RegistrationForm, LoginForm


def index(request):
    """Index page of user map.

    :param request: A django request object.
    :type request: request

    :returns: Response will be a nice looking map page.
    :rtype: HttpResponse
    """
    return HttpResponse("Hello, world. You're at the user_map index.")


def register(request):
    """User registration view.

    :param request: A django request object.
    :type request: request
    """
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse('user_map:index'))
    else:
        form = RegistrationForm()
    return render_to_response('user_map/register.html', {
        'form': form,
    }, context_instance=RequestContext(request))


def login(request):
    """Login view.

    :param request: A django request object.
    :type request: request
    """
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                email=request.POST['email'],
                password=request.POST['password']
            )
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    return HttpResponseRedirect(reverse('user_map:index'))
    else:
        form = LoginForm()
    return render_to_response(
        'user_map/login.html',
        {'form': form},
        context_instance=RequestContext(request))


def logout(request):
    """
    Log out view
    """
    django_logout(request)
    return HttpResponseRedirect(reverse('user_map:index'))
