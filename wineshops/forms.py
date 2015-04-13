# -*- coding: utf8 -*-
__author__ = 'Sylvain'
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from .models import Shop, Wine

class WineshopForm(ModelForm):

    class Meta:
        model = Shop
        fields = ['name', 'address', 'city', 'zip_code', 'country', 'description', 'phone', 'mail', 'web']

class WineForm(ModelForm):
    class Meta:
        model=Wine
        fields = '__all__'

ShopFormSet = inlineformset_factory(Shop, Wine, fields='__all__')