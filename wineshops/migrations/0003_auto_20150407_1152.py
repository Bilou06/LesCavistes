# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0002_auto_20150407_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='description',
            field=models.TextField(max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='mail',
            field=models.EmailField(max_length=254, blank=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='phone',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='web',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='wine',
            name='classification',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
