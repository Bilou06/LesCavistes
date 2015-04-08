# -*- coding: utf8 -*-
__author__ = 'Sylvain'

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'E-mail address'}))
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')


    #clean email field
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("Cet e-mail est déjà utilisé, merci d'en saisir un autre ou d'utiliser la fonction \"mot de passe oublié\".")

    #clean username field
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
              User.objects.get(username=username)
        except User.DoesNotExist:
              return username
        raise forms.ValidationError("Cet identifiant est déjà utilisé, merci d'en choisir un autre.")

    #clean password field
    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if not password1:
            raise forms.ValidationError("Entrez un mot de passe.")
        if len(password1)<7:
            raise forms.ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data['password2']
        if not password2:
            raise forms.ValidationError("Confirmez le mot de passe.")
        return password2

    #modify save() method so that we can set user.is_active to False when we first create our user
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False # not active until he opens activation link
            user.save()

        return user



class PickyAuthenticationForm(AuthenticationForm):
    pass