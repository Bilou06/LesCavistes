# -*- coding: utf-8 -*-
__author__ = 'Sylvain'

from django import forms
from django.forms import ModelForm, HiddenInput
from .models import Shop, Wine


class WineshopForm(ModelForm):

    class Meta:
        model = Shop
        fields = ['name', 'address', 'zip_code', 'city', 'country', 'description', 'phone', 'mail', 'web', 'latitude', 'longitude']
        widgets = {
            'latitude' : HiddenInput(),
            'longitude' : HiddenInput(),
        }
#

class WineForm(ModelForm):
    class Meta:
        model = Wine
        exclude = ['shop']

    country_hidden = forms.CharField(widget=forms.HiddenInput, required=False)
    region_hidden = forms.CharField(widget=forms.HiddenInput, required=False)
    area_hidden = forms.CharField(widget=forms.HiddenInput, required=False)

