# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0023_auto_20150521_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wine',
            name='capacity',
            field=models.ForeignKey(to='wineshops.Capacity', null=True, verbose_name='Contenance', blank=True),
        ),
        migrations.AlterField(
            model_name='wine',
            name='color',
            field=models.ForeignKey(to='wineshops.Color', null=True, verbose_name='Couleur', blank=True),
        ),
    ]
