# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wineshops', '0006_auto_20150409_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='user',
            field=models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shop',
            name='address',
            field=models.CharField(max_length=250, verbose_name='Adresse'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='city',
            field=models.CharField(max_length=100, verbose_name='Ville'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='country',
            field=models.CharField(max_length=100, verbose_name='Pays', default='France'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='description',
            field=models.TextField(max_length=500, verbose_name='Déscription', blank=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='mail',
            field=models.EmailField(max_length=254, verbose_name='E-mail', blank=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='phone',
            field=models.CharField(max_length=20, verbose_name='Téléphone', blank=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='web',
            field=models.CharField(max_length=50, verbose_name='Site web', blank=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='zip_code',
            field=models.IntegerField(verbose_name='Code postal'),
        ),
    ]
