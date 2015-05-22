# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0029_auto_20150521_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='image',
            field=models.ImageField(null=True, width_field=140, upload_to='', verbose_name='Image', height_field=140),
        ),
    ]
