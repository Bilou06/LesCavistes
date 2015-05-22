# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wineshops.models


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0032_auto_20150522_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='image',
            field=models.ImageField(upload_to=wineshops.models.user_directory_path, blank=True, null=True, verbose_name='Image', default='media/None/default.png'),
        ),
    ]
