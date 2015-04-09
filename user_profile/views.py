# -*- coding: utf8 -*-
import hashlib
import random
import datetime

from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.template import RequestContext
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
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
                         % (user.user.username, user.activation_key)

            sendmail(email_subject, email_body, email)

            return HttpResponseRedirect('/user/register_success')
    else:
        args['form'] = RegistrationForm()

    return render_to_response('user_profile/register.html', args, context_instance=RequestContext(request))


def resend_mail(request):
    user = get_object_or_404(UserProfile, request.POST['userId'])

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
        send_mail(subject, body, 'myemail@example.com',
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
                    return HttpResponseRedirect('/')
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


def account(request):
    return HttpResponse('account')