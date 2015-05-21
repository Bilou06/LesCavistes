# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0026_auto_20150521_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='capacity',
            name='volume',
            field=models.IntegerField(default=75, verbose_name='Contenance'),
        ),
    ]
