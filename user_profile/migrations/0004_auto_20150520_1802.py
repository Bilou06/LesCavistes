# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_auto_20150410_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='VAT',
            field=models.CharField(max_length=13, default='', verbose_name='TVA'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.CharField(max_length=250, default='', verbose_name='Adresse'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='city',
            field=models.CharField(max_length=100, default='', verbose_name='Ville'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='name',
            field=models.CharField(max_length=40, default='', verbose_name='Dénomination sociale'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='zip_code',
            field=models.IntegerField(default=0, verbose_name='Code postal'),
        ),
    ]
