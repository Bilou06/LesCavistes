# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0010_auto_20150409_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='address',
            field=models.CharField(null=True, verbose_name='Adresse', max_length=250),
        ),
        migrations.AlterField(
            model_name='shop',
            name='city',
            field=models.CharField(null=True, verbose_name='Ville', max_length=100),
        ),
        migrations.AlterField(
            model_name='shop',
            name='description',
            field=models.TextField(null=True, verbose_name='Déscription', blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='shop',
            name='mail',
            field=models.EmailField(null=True, verbose_name='E-mail', blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='shop',
            name='name',
            field=models.CharField(null=True, verbose_name='Nom', max_length=100),
        ),
        migrations.AlterField(
            model_name='shop',
            name='phone',
            field=models.CharField(null=True, verbose_name='Téléphone', blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='shop',
            name='web',
            field=models.CharField(null=True, verbose_name='Site web', blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='shop',
            name='zip_code',
            field=models.IntegerField(null=True, verbose_name='Code postal'),
        ),
    ]
