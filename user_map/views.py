# coding=utf-8
"""Views of the apps."""
import csv
import json

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.forms.util import ErrorList
from django.forms.forms import NON_FIELD_ERRORS
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import (
    login as django_login,
    authenticate,
    logout as django_logout)
from django.contrib.auth.views import (
    password_reset as django_password_reset,
    password_reset_done as django_password_reset_done,
    password_reset_confirm as django_password_reset_confirm,
    password_reset_complete as django_password_reset_complete)
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.models import get_current_site

from user_map.forms import (
    RegistrationForm,
    LoginForm,
    BasicInformationForm,
    CustomPasswordResetForm)
from user_map.models import User
from user_map.app_settings import (
    PROJECT_NAME, DEFAULT_FROM_MAIL, LEAFLET_TILES)
from user_map.utilities.decorators import login_forbidden


def index(request):
    """Index page of user map.

    :param request: A django request object.
    :type request: request

    :returns: Response will be a nice looking map page.
    :rtype: HttpResponse
    """
    information_modal = loader.render_to_string(
        'user_map/information_modal.html')
    data_privacy_content = loader.render_to_string(
        'user_map/data_privacy.html')

    user_menu_button = loader.render_to_string(
        'user_map/user_menu_button.html', {'user': request.user})

    leaflet_tiles = dict(
        url=LEAFLET_TILES[1],
        attribution=LEAFLET_TILES[2]
    )
    context = {
        'data_privacy_content': data_privacy_content,
        'information_modal': information_modal,
        'user_menu_button': user_menu_button,
        'leaflet_tiles': leaflet_tiles
    }
    return render(request, 'user_map/index.html', context)


def get_users(request):
    """Return a json document of all users.

    This will only fetch users who have approved by email and still active.

    :param request: A django request object.
    :type request: request
    """
    if request.method == 'GET':
        # Get user
        users = User.objects.filter(
            is_confirmed=True,
            is_active=True)
        users_json = loader.render_to_string(
            'user_map/users.json', {'users': users})

        # Return Response
        return HttpResponse(users_json, content_type='application/json')
    else:
        raise Http404


@login_forbidden
def register(request):
    """User registration view.

    :param request: A django request object.
    :type request: request
    """
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            form.save_m2m()

            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
            context = {
                'project_name': PROJECT_NAME,
                'protocol': 'http',
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'key': user.key
            }
            email = loader.render_to_string(
                'user_map/account/registration_confirmation_email.html',
                context)

            subject = '%s User Registration' % PROJECT_NAME
            sender = '%s - No Reply <%s>' % (PROJECT_NAME, DEFAULT_FROM_MAIL)
            send_mail(
                subject, email, sender, [user.email], fail_silently=False)

            messages.success(
                request,
                ('Thank you for registering in our site! Please check your '
                 'email to confirm your registration'))
            return HttpResponseRedirect(reverse('user_map:register'))
    else:
        form = RegistrationForm()
    return render_to_response(
        'user_map/account/registration.html',
        {'form': form},
        context_instance=RequestContext(request)
    )


@login_forbidden
def confirm_registration(request, uid, key):
    """The view containing form to reset password and process it.

    :param request: A django request object.
    :type request: request

    :param uid: A unique id for a user.
    :type uid: str

    :param key: Key to confirm the user.
    :type key: str
    """
    decoded_uid = urlsafe_base64_decode(uid)
    try:
        user = User.objects.get(pk=decoded_uid)

        if not user.is_confirmed:
            if user.key == key:
                user.is_confirmed = True
                user.save(update_fields=['is_confirmed'])
                information = (
                    'Congratulations! Your account has been successfully '
                    'confirmed. Please continue to log in.')
            else:
                information = (
                    'Your link is not valid. Please make sure that you use '
                    'confirmation link we sent to your email.')
        else:
            information = ('Your account is already confirmed. Please '
                           'continue to log in.')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        information = ('Your link is not valid. Please make sure that you use '
                       'confirmation link we sent to your email.')

    context = {
        'page_header_title': 'Registration Confirmation',
        'information': information
    }
    return render_to_response(
        'user_map/information.html',
        context,
        context_instance=RequestContext(request)
    )


@login_forbidden
def login(request):
    """Login view.

    :param request: A django request object.
    :type request: request
    """
    if request.method == 'POST':
        next_page = request.GET.get('next', '')
        if next_page == '':
            next_page = reverse('user_map:index')
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                email=request.POST['email'],
                password=request.POST['password']
            )
            if user is not None:
                if user.is_active and user.is_confirmed:
                    django_login(request, user)

                    return HttpResponseRedirect(next_page)
                if not user.is_active:
                    errors = form._errors.setdefault(
                        NON_FIELD_ERRORS, ErrorList())
                    errors.append(
                        'The user is not active. Please contact our '
                        'administrator to resolve this.')
                if not user.is_confirmed:
                    errors = form._errors.setdefault(
                        NON_FIELD_ERRORS, ErrorList())
                    errors.append(
                        'Please confirm you registration email first!')
            else:
                errors = form._errors.setdefault(
                    NON_FIELD_ERRORS, ErrorList())
                errors.append(
                    'Please enter a correct email and password. '
                    'Note that both fields may be case-sensitive.')
    else:
        form = LoginForm()

    return render_to_response(
        'user_map/account/login.html',
        {'form': form},
        context_instance=RequestContext(request))


def logout(request):
    """Log out view.

    :param request: A django request object.
    :type request: request
    """
    django_logout(request)
    return HttpResponseRedirect(reverse('user_map:index'))


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
                basic_info_form.save_m2m()
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


@login_required(login_url='user_map:index')
def delete_user(request):
    """Delete user view.

    :param request: A django request object.
    :type request: request
    """
    if request.method == 'POST':
        user = request.user
        user.delete()
        django_logout(request)

        information = ('You have deleted your account. Please register to '
                       'this site any time you want.')
        context = {
            'page_header_title': 'Delete Account',
            'information': information
        }
        return render_to_response(
            'user_map/information.html',
            context,
            context_instance=RequestContext(request)
        )
    else:
        raise Http404


@login_forbidden
def password_reset(request):
    """The view for reset password that contains a form to ask for email.

    :param request: A django request object.
    :type request: request
    """
    return django_password_reset(
        request,
        password_reset_form=CustomPasswordResetForm,
        template_name='user_map/account/password_reset_form.html',
        email_template_name='user_map/account/password_reset_email.html',
        post_reset_redirect=reverse('user_map:password_reset_done'))


@login_forbidden
def password_reset_done(request):
    """The view telling the user that an email has been sent.

    :param request: A django request object.
    :type request: request
    """
    return django_password_reset_done(
        request,
        template_name='user_map/account/password_reset_done.html')


@login_forbidden
def password_reset_confirm(request, uidb64=None, token=None):
    """The view containing form to reset password and process it.

    :param request: A django request object.
    :type request: request

    :param uidb64: An unique ID of the user.
    :type uidb64: str

    :param token: Token to check if the reset password link is valid.
    :type token: str
    """
    return django_password_reset_confirm(
        request,
        uidb64=uidb64,
        token=token,
        template_name='user_map/account/password_reset_confirm.html',
        set_password_form=SetPasswordForm,
        post_reset_redirect=reverse('user_map:password_reset_complete'))


@login_forbidden
def password_reset_complete(request):
    """The view telling the user that reset password has been completed.

    :param request: A django request object.
    :type request: request
    """
    return django_password_reset_complete(
        request,
        template_name='user_map/account/password_reset_complete.html')


def download(request):
    """The view to download users data as CSV.

    :param request: A django request object.
    :type request: request

    :return: A CSV file.
    :type: HttpResponse
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    users = User.objects.filter(roles__sort_number__gte=1).distinct()
    writer = csv.writer(response)

    fields = ['name', 'website', 'location']
    headers = ['No.']
    for field in fields:
        verbose_name_field = users.model._meta.get_field(field).verbose_name
        headers.append(verbose_name_field)
    headers.append('Role(s)')
    writer.writerow(headers)

    for idx, user in enumerate(users):
        row = [idx + 1]
        for field in fields:
            field_value = getattr(user, field)
            row.append(field_value)
        row.append(user.get_roles())
        writer.writerow(row)

    return response
