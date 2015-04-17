# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0014_auto_20150415_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='longitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='description',
            field=models.TextField(verbose_name='Description', blank=True, max_length=500, null=True),
        ),
    ]
