# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0013_auto_20150413_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='wine',
            name='varietal',
            field=models.CharField(max_length=250, verbose_name='Cépage', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wine',
            name='area',
            field=models.ForeignKey(verbose_name='Terroir', to='wineshops.Area'),
        ),
        migrations.AlterField(
            model_name='wine',
            name='capacity',
            field=models.IntegerField(default=75, verbose_name='Contenance'),
        ),
        migrations.AlterField(
            model_name='wine',
            name='classification',
            field=models.CharField(max_length=50, verbose_name='Classification', blank=True),
        ),
        migrations.AlterField(
            model_name='wine',
            name='color',
            field=models.ForeignKey(verbose_name='Couleur', to='wineshops.Color'),
        ),
        migrations.AlterField(
            model_name='wine',
            name='price_max',
            field=models.FloatField(verbose_name='Prix maximum', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wine',
            name='price_min',
            field=models.FloatField(verbose_name='Prix minimum', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wine',
            name='producer',
            field=models.CharField(max_length=50, verbose_name='Producteur', blank=True),
        ),
        migrations.AlterField(
            model_name='wine',
            name='vintage',
            field=models.IntegerField(verbose_name='Millésime', blank=True, null=True),
        ),
    ]
