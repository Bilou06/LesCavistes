# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0017_auto_20150420_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='custom',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='country',
            name='custom',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='region',
            name='custom',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='area',
            name='name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='region',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='wine',
            name='area',
            field=models.ForeignKey(to='wineshops.Area', blank=True, verbose_name='Terroir'),
        ),
        migrations.AlterField(
            model_name='wine',
            name='country',
            field=models.ForeignKey(to='wineshops.Country', blank=True, verbose_name='Pays'),
        ),
        migrations.AlterField(
            model_name='wine',
            name='region',
            field=models.ForeignKey(to='wineshops.Region', blank=True, verbose_name='Région'),
        ),
    ]
