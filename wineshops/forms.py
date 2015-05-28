# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

__author__ = 'Sylvain'

from django import forms
from django.forms import ModelForm, HiddenInput
from .models import Shop, Wine



class ImageWidget(forms.FileInput):
    """
    A ImageField Widget that shows a thumbnail.
    """

    def __init__(self, attrs={}):
        super(ImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append(('Actuellement: <a target="_blank" href="%s">'
                           '<img src="%s" style="height: 28px;" /></a>'
                           '<input id="image-clear_id" name="image-clear" type="checkbox">'
                           '<label for="image-clear_id">Effacer</label><br>Modifier: '
                           % (value.url, value.url)))
        output.append(super(ImageWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class WineshopForm(ModelForm):

    class Meta:
        model = Shop
        fields = ['name', 'address', 'zip_code', 'city', 'country', 'description', 'phone', 'mail', 'web', 'latitude', 'longitude', 'image']
        widgets = {
            'latitude': HiddenInput(),
            'longitude': HiddenInput(),
            'image' : ImageWidget
        }

    def clean_image(self):
        image = self.image
        if image:
            from django.core.files.images import get_image_dimensions

            sub = image.name.split('.')[-1]
            if not (sub.lower() in ['gif', 'jpeg', 'pjpeg', 'png', 'jpg']):
                raise forms.ValidationError(u"Format d'image invalide : veuillez séléctionner un fichier .gif, .jpg, .jpeg, .pjpeg, ou .png." )

            #if len(image) > 1*1024*1024:
            #    raise ValidationError("Image trop volumineuse ( maximum 1mb )")

            return image


class WineForm(ModelForm):
    class Meta:
        model = Wine
        exclude = ['shop']

    country_hidden = forms.CharField(widget=forms.HiddenInput, required=False)
    region_hidden = forms.CharField(widget=forms.HiddenInput, required=False)
    area_hidden = forms.CharField(widget=forms.HiddenInput, required=False)
    color_hidden = forms.CharField(widget=forms.HiddenInput, required=False)
    capacity_hidden = forms.FloatField(widget=forms.HiddenInput, required=False)

