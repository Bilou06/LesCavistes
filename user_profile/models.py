# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=now)

    name        = models.CharField(max_length=40, verbose_name="Dénomination sociale")
    address     = models.CharField(max_length = 250, verbose_name="Adresse")
    city        = models.CharField(max_length = 100, verbose_name="Ville")
    zip_code    = models.IntegerField(verbose_name="Code postal")
    country     = models.CharField(max_length = 100, default = 'France', verbose_name="Pays")
    VAT         = models.CharField(max_length=13, verbose_name="TVA")


    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = u"Profile utilisateur"
        verbose_name_plural = u'Profiles utilisateur'