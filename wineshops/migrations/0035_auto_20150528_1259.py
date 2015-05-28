# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields
import wineshops.models


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0034_auto_20150528_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='image_hdpi',
            field=imagekit.models.fields.ProcessedImageField(default='media/None/default.png', null=True, verbose_name='Image', blank=True, upload_to=wineshops.models.user_directory_path_hdpi),
        ),
        migrations.AddField(
            model_name='shop',
            name='image_ldpi',
            field=imagekit.models.fields.ProcessedImageField(default='media/None/default.png', null=True, verbose_name='Image', blank=True, upload_to=wineshops.models.user_directory_path_ldpi),
        ),
        migrations.AddField(
            model_name='shop',
            name='image_mdpi',
            field=imagekit.models.fields.ProcessedImageField(default='media/None/default.png', null=True, verbose_name='Image', blank=True, upload_to=wineshops.models.user_directory_path_mdpi),
        ),
        migrations.AddField(
            model_name='shop',
            name='image_xhdpi',
            field=imagekit.models.fields.ProcessedImageField(default='media/None/default.png', null=True, verbose_name='Image', blank=True, upload_to=wineshops.models.user_directory_path_xhdpi),
        ),
    ]
