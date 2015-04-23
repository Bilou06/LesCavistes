#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Sylvain'

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from captcha.fields import ReCaptchaField
from django.utils.translation import ugettext, ugettext_lazy as _


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput())
    first_name = forms.CharField(required=False, label='Prénom')
    last_name = forms.CharField(required=False, label='Nom')
    captcha = ReCaptchaField(attrs={'label' : 'Êtes-vous humain ?', 'theme' : 'clean'})
    contract_check = forms.BooleanField(required = True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    # clean email field
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            "Cet e-mail est déjà utilisé, merci d'en saisir un autre ou d'utiliser la/"
            " fonction \"mot de passe oublié\".")

    # clean username field
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Cet identifiant est déjà utilisé, merci d'en choisir un autre.")

    # clean password field
    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if not password1:
            raise forms.ValidationError("Entrez un mot de passe.")
        if len(password1) < 7:
            raise forms.ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data['password2']
        if not password2:
            raise forms.ValidationError("Confirmez le mot de passe.")
        return password2

    # modify save() method so that we can set user.is_active to False when we first create our user
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False  # not active until he opens activation link
            user.save()

        return user


class EditUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'E-mail address'}), label="E-mail")
    first_name = forms.CharField(required=False, label="Prénom")
    last_name = forms.CharField(required=False, label="Nom")
    username = forms.CharField(max_length=254, label="Identifiant")
    last_login = forms.DateTimeField(label="Dernière connexion")

    class Meta:
        model = User
        fields = ('username', 'email', 'last_login', 'last_name', 'first_name', )

    email.widget.attrs['readonly'] = True
    username.widget.attrs['readonly'] = True
    last_login.widget.attrs['readonly'] = True

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class PickyAuthenticationForm(AuthenticationForm):
    pass

class FrenchPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        'password_mismatch': "Les deux mots de passe ne correspondent pas.",
        'password_incorrect': "Votre ancien mot de passe ne correspond pas. "
                "Merci d'essayer à nouveau.",
    }

class FrenchPasswordResetForm(PasswordResetForm):
    pass

class FrenchSetPasswordForm(SetPasswordForm):
    pass