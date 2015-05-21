# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0028_auto_20150521_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capacity',
            name='volume',
            field=models.FloatField(verbose_name='Contenance', null=True, blank=True, default=75),
        ),
    ]
