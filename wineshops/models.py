# -*- coding: utf8 -*-

import datetime
from django.db import models
from django.contrib.auth.models import User


class Shop(models.Model):
    name        = models.CharField(max_length = 100, verbose_name="Nom")
    address     = models.CharField(max_length = 250, verbose_name="Adresse")
    city        = models.CharField(max_length = 100, verbose_name="Ville")
    zip_code    = models.IntegerField(verbose_name="Code postal")
    country     = models.CharField(max_length = 100, default = 'France', verbose_name="Pays")
    description = models.TextField(max_length = 500, blank = True, verbose_name="Déscription")
    phone       = models.CharField(max_length = 20, blank = True, verbose_name="Téléphone")
    mail        = models.EmailField(blank = True, verbose_name="E-mail")
    web         = models.CharField(max_length = 50, blank = True, verbose_name="Site web")
    user        = models.ForeignKey(User)

    def __str__(self):
        return self.name

class Country(models.Model):#France, ...
    name        = models.CharField(max_length = 50, unique = True)

    def __str__(self):
        return self.name

class Region(models.Model):#Bordeaux, ...
    country     = models.ForeignKey(Country)
    name        = models.CharField(max_length = 50, unique = True)

    def __str__(self):
        return self.name

class Area(models.Model):#Saint-estèphe ...
    region      = models.ForeignKey(Region)
    name        = models.CharField(max_length = 50, unique = True)

    def __str__(self):
        return self.name

class Color(models.Model):
    name        = models.CharField(max_length = 20, unique = True)

    def __str__(self):
        return self.name

class Wine(models.Model):
    shop        = models.ForeignKey(Shop)
    producer    = models.CharField(max_length = 50, blank = True )
    area        = models.ForeignKey(Area)
    vintage     = models.IntegerField(blank = True)
    classification = models.CharField(max_length = 50, blank = True )
    color       = models.ForeignKey(Color)
    capacity    = models.IntegerField(default = 75)
    price_min   = models.FloatField(blank = True, null=True)
    price_max   = models.FloatField(blank = True, null=True)

    def __str__(self):
        return self.producer + ' ' + self.vintage




