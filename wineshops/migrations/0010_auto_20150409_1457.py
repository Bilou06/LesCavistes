# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0009_shop_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='address',
            field=models.CharField(verbose_name='Adresse', max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='city',
            field=models.CharField(verbose_name='Ville', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='name',
            field=models.CharField(verbose_name='Nom', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='zip_code',
            field=models.IntegerField(verbose_name='Code postal', blank=True),
        ),
    ]
