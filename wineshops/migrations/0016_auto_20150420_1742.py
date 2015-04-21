# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0015_auto_20150417_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='wine',
            name='country',
            field=models.CharField(unique=True, default='', verbose_name='Pays', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wine',
            name='region',
            field=models.CharField(unique=True, default='', verbose_name='Région', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='wine',
            name='area',
            field=models.CharField(unique=True, verbose_name='Terroir', max_length=50),
        ),
    ]
