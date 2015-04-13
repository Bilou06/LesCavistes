# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0012_auto_20150413_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wine',
            name='vintage',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
