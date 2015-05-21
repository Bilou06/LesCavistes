# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0027_capacity_volume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capacity',
            name='volume',
            field=models.FloatField(verbose_name='Contenance', default=75),
        ),
    ]
