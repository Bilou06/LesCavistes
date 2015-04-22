# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0019_auto_20150421_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='wine',
            name='in_stock',
            field=models.BooleanField(default=True, verbose_name='En stock'),
        ),
    ]
