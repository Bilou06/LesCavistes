# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0025_auto_20150521_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]
