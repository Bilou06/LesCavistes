# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0007_auto_20150409_1452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='user',
        ),
    ]
