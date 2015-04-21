# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0016_auto_20150420_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wine',
            name='area',
            field=models.CharField(max_length=50, verbose_name='Terroir'),
        ),
        migrations.AlterField(
            model_name='wine',
            name='country',
            field=models.CharField(max_length=50, verbose_name='Pays'),
        ),
        migrations.AlterField(
            model_name='wine',
            name='region',
            field=models.CharField(max_length=50, verbose_name='Région'),
        ),
    ]
