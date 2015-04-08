# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('country', models.ForeignKey(to='wineshops.Country')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=250)),
                ('city', models.CharField(max_length=100)),
                ('zip_code', models.IntegerField()),
                ('description', models.TextField(max_length=500)),
                ('phone', models.CharField(max_length=20)),
                ('mail', models.EmailField(max_length=254)),
                ('web', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Wine',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('producer', models.CharField(max_length=50)),
                ('vintage', models.IntegerField()),
                ('classification', models.CharField(max_length=50)),
                ('capacity', models.IntegerField(default=75)),
                ('area', models.ForeignKey(to='wineshops.Area')),
                ('color', models.ForeignKey(to='wineshops.Color')),
                ('shop', models.ForeignKey(to='wineshops.Shop')),
            ],
        ),
        migrations.AddField(
            model_name='area',
            name='region',
            field=models.ForeignKey(to='wineshops.Region'),
        ),
    ]
