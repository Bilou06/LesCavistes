# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields
import wineshops.models


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0033_auto_20150522_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(default='media/None/default.png', null=True, blank=True, verbose_name='Image', upload_to=wineshops.models.user_directory_path),
        ),
    ]
