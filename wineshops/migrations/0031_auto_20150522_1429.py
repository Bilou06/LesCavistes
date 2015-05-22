# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0030_shop_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='image',
            field=models.ImageField(upload_to='media/', height_field=140, blank=True, null=True, verbose_name='Image', default='media/None/default.png', width_field=140),
        ),
    ]
