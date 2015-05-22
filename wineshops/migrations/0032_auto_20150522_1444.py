# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0031_auto_20150522_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='image',
            field=models.ImageField(upload_to='media/', blank=True, default='media/None/default.png', null=True, verbose_name='Image'),
        ),
    ]
