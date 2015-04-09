# -*- coding: utf8 -*-
__author__ = 'Sylvain'
from django.forms import ModelForm
from .models import Shop



class WineshopForm(ModelForm):

    class Meta:
        model = Shop
        fields = ['name', 'address', 'city', 'zip_code', 'country', 'description', 'phone', 'mail', 'web']

