# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wineshops', '0022_auto_20150520_1739'),
    ]

    operations = [
        migrations.CreateModel(
            name='Capacity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('volume', models.IntegerField(verbose_name='Contenance', default=75)),
            ],
        ),
        migrations.AddField(
            model_name='color',
            name='custom',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='wine',
            name='capacity',
            field=models.ForeignKey(to='wineshops.Capacity', verbose_name='Contenance'),
        ),
    ]
