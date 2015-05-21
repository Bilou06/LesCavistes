# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0021_shop_filled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='name',
            field=models.CharField(verbose_name='Nom du magasin', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='wine',
            name='area',
            field=models.ForeignKey(null=True, blank=True, verbose_name='Appellations', to='wineshops.Area'),
        ),
        migrations.AlterField(
            model_name='wine',
            name='region',
            field=models.ForeignKey(null=True, blank=True, verbose_name='Vignoble', to='wineshops.Region'),
        ),
    ]
