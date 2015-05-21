# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0024_auto_20150521_1113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='capacity',
            name='volume',
        ),
        migrations.AddField(
            model_name='capacity',
            name='custom',
            field=models.BooleanField(default=False),
        ),
    ]
