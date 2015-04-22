# -*- coding: utf-8 -*-
import hashlib
import random
import datetime

from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.core.mail import send_mail
from django.core.context_processors import csrf
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth.tokens import default_token_generator

import logging

from trouvetonvin.settings import DEBUG

from user_profile.forms import *
from .models import UserProfile


def register_user(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        args['form'] = form
        if form.is_valid():
            form.save()  # save user to database if form is valid

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            random_string = str(random.random()).encode('utf8')
            salt = hashlib.sha1(random_string).hexdigest()[:5]
            salted = (salt + email).encode('utf8')
            activation_key = hashlib.sha1(salted).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            # Get user by username
            user = User.objects.get(username=username)

            # Create and save user profile
            new_profile = UserProfile(user=user, activation_key=activation_key,
                                      key_expires=key_expires)
            new_profile.save()

            # Send email with activation key
            email_subject = 'Account confirmation'
            email_body = "Hey %s, merci de vous être inscrit. Pour activer votre compte, \
                    cliquez sur le lien avant 48 heures http://127.0.0.1:8000/user/confirm/%s" \
                         % (user.username, activation_key)

            sendmail(email_subject, email_body, email)

            return HttpResponseRedirect('/user/register_success')
    else:
        args['form'] = RegistrationForm()

    return render_to_response('user_profile/register.html', args, context_instance=RequestContext(request))


def resend_mail(request):
    user = get_object_or_404(UserProfile, pk=request.POST['userId'])

    email = user.user.email
    random_string = str(random.random()).encode('utf8')
    salt = hashlib.sha1(random_string).hexdigest()[:5]
    salted = (salt + email).encode('utf8')
    user.activation_key = hashlib.sha1(salted).hexdigest()
    user.key_expires = datetime.datetime.today() + datetime.timedelta(2)
    user.save()

    # Send email with activation key
    email_subject = 'Account confirmation'
    email_body = "Hey %s, merci de vous être inscrit. Pour activer votre compte, cliquez sur le lien avant 48 heures\
            http://127.0.0.1:8000/user/confirm/%s" % (user.user.username, user.activation_key)

    sendmail(email_subject, email_body, email)

    return HttpResponseRedirect('/user/register_success')


def sendmail(subject, body, email):
    logger = logging.getLogger(__name__)
    logger.info('|'.join(['EMAIL ', email, subject, body]))
    if not DEBUG:
        send_mail(subject, body, 'myemail@example.com', #  TODO : change mail
                  [email], fail_silently=False)


def register_confirm(request, activation_key):
    # check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect('/home')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    # check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        return render(request, 'user_profile/confirm_expired.html', {'user': user_profile})
    # if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('user_profile/confirm.html')


def register_success(request):
    return render(request, 'user_profile/register_success.html')


def log_in(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = PickyAuthenticationForm(data=request.POST)
        args['form'] = form
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/wineshops/edit/')
                else:
                    return HttpResponse('compte inactif')
            else:
                # Return an 'invalid login' error message.
                args['errors'] = 'L\'identifiant et le mot de passe ne correspondent pas'
    else:
        args['form'] = PickyAuthenticationForm()

    return render(request, 'user_profile/login.html', args)


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')



@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request):

    template_name='user_profile/password.html'

    if request.method == "POST":
        form = FrenchPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one if
            # django.contrib.auth.middleware.SessionAuthenticationMiddleware
            # is enabled.
            update_session_auth_hash(request, form.user)
            return render(request, 'user_profile/password_change_done.html')
    else:
        form = FrenchPasswordChangeForm(user=request.user)
    context = {
        'form': form,
    }

    return TemplateResponse(request, template_name, context)





# 4 views for password reset:
# - password_reset sends the mail
# - password_reset_done shows a success message for the above
# - password_reset_confirm checks the link the user clicked and
#   prompts for a new password
# - password_reset_complete shows a success message for the above

@csrf_protect
def password_reset(request, is_admin_site=False,
                   template_name='user_profile/password_reset_form.html',
                   email_template_name='user_profile/password_reset_email.html',
                   subject_template_name='user_profile/password_reset_subject.txt',
                   token_generator=default_token_generator,
                   from_email=None, #  TODO set a correct e-mail
                   html_email_template_name=None):


    if request.method == "POST":
        form = FrenchPasswordResetForm(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            form.save(**opts)
            return HttpResponseRedirect('/user_profile/password_reset_done/')
    else:
        form = FrenchPasswordResetForm()
    context = {
        'form': form,
        'title': _('Réinitialisation du mot de passe'),
    }

    return TemplateResponse(request, template_name, context)


def password_reset_done(request,
                        template_name='user_profile/password_reset_done.html',
                        current_app=None, extra_context=None):
    context = {
        'title': _('Réinitialisation du mot de passe envoyée'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb64=None, token=None,
                           template_name='user_profile/password_reset_confirm.html',
                           token_generator=default_token_generator):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = _('Entrez le nouveau mot de passe')
        if request.method == 'POST':
            form = FrenchSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/user_profile/password_reset_complete/')
        else:
            form = FrenchSetPasswordForm(user)
    else:
        validlink = False
        form = None
        title = _("Impossible d'entrer le nouveau mot de passe")
    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
    }

    return TemplateResponse(request, template_name, context)


def password_reset_complete(request,
                            template_name='user_profile/password_reset_complete.html',):
    context = {
        'login_url': 'user_profile/login',
        'title': _('Mot de passe changé'),
    }

    return TemplateResponse(request, template_name, context)



def contract(request):
    return TemplateResponse(request, 'user_profile/contract.html')