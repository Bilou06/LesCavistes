# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0004_auto_20150520_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='country',
            field=models.CharField(default='France', max_length=100, verbose_name='Pays'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='VAT',
            field=models.CharField(max_length=13, verbose_name='TVA'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.CharField(max_length=250, verbose_name='Adresse'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(max_length=100, verbose_name='Ville'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(max_length=40, verbose_name='Dénomination sociale'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='zip_code',
            field=models.IntegerField(verbose_name='Code postal'),
        ),
    ]
