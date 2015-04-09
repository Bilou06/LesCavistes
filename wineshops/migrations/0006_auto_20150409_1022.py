# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0005_auto_20150407_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='wine',
            name='price_max',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wine',
            name='price_min',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wine',
            name='vintage',
            field=models.IntegerField(blank=True),
        ),
    ]
