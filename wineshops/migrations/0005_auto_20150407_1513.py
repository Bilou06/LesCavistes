# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0004_shop_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wine',
            name='producer',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
