# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0020_wine_in_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='filled',
            field=models.BooleanField(default=False),
        ),
    ]
