# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0018_auto_20150421_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wine',
            name='area',
            field=models.ForeignKey(null=True, to='wineshops.Area', verbose_name='Terroir', blank=True),
        ),
        migrations.AlterField(
            model_name='wine',
            name='country',
            field=models.ForeignKey(null=True, to='wineshops.Country', verbose_name='Pays', blank=True),
        ),
        migrations.AlterField(
            model_name='wine',
            name='region',
            field=models.ForeignKey(null=True, to='wineshops.Region', verbose_name='Région', blank=True),
        ),
    ]
