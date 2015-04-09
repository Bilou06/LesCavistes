# -*- coding: utf8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=now)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = u"Profile utilisateur"
        verbose_name_plural = u'Profiles utilisateur'