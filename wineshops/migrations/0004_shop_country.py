# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0003_auto_20150407_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='country',
            field=models.CharField(default='France', max_length=100),
        ),
    ]
