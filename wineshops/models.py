# -*- coding: utf8 -*-
from django.db import models
from django.contrib.auth.models import User



class Shop(models.Model):
    name        = models.CharField(max_length = 100, verbose_name="Nom", null=True)
    address     = models.CharField(max_length = 250, verbose_name="Adresse", null=True)
    city        = models.CharField(max_length = 100, verbose_name="Ville", null=True)
    zip_code    = models.IntegerField(verbose_name="Code postal", null=True)
    country     = models.CharField(max_length = 100, default = 'France', verbose_name="Pays")
    description = models.TextField(max_length = 500, blank = True, verbose_name="Description", null=True)
    phone       = models.CharField(max_length = 20, blank = True, verbose_name="Téléphone", null=True)
    mail        = models.EmailField(blank = True, verbose_name="E-mail", null=True)
    web         = models.CharField(max_length = 50, blank = True, verbose_name="Site web", null=True)
    user        = models.ForeignKey(User)
    latitude    = models.FloatField(null=True)
    longitude   = models.FloatField(null=True)

    def __str__(self):
        if self.name:
            return self.name
        return ''

class Country(models.Model):#  France, ...
    name        = models.CharField(max_length = 50, unique = True)
    custom      = models.BooleanField(default=False)#  custom = False -> appear in combo box for everyone

    def __str__(self):
        return self.name

class Region(models.Model):#  Bordeaux, ...
    country     = models.ForeignKey(Country)
    name        = models.CharField(max_length = 50)
    custom      = models.BooleanField(default=False)#  custom = False -> appear in combo box for everyone

    def __str__(self):
        return self.name

class Area(models.Model):#  Saint-estèphe ...
    region      = models.ForeignKey(Region)
    name        = models.CharField(max_length = 50)
    custom      = models.BooleanField(default=False)#  custom = False -> appear in combo box for everyone

    def __str__(self):
        return self.name

class Color(models.Model):
    name        = models.CharField(max_length = 20, unique = True)

    def __str__(self):
        return self.name

class Wine(models.Model):
    shop        = models.ForeignKey(Shop)
    producer    = models.CharField(max_length = 50, blank = True, verbose_name="Producteur")
    country     = models.ForeignKey(Country, verbose_name="Pays", blank=True)
    region      = models.ForeignKey(Region, verbose_name="Région", blank=True)
    area        = models.ForeignKey(Area, verbose_name="Terroir", blank=True)
    vintage     = models.IntegerField(blank = True, null=True, verbose_name="Millésime")
    classification = models.CharField(max_length = 50, blank = True, verbose_name="Classification" )
    color       = models.ForeignKey(Color, verbose_name="Couleur")
    varietal    = models.CharField(max_length=250, blank=True, null=True, verbose_name="Cépage")
    capacity    = models.IntegerField(default = 75, verbose_name="Contenance")
    price_min   = models.FloatField(blank = True, null=True, verbose_name="Prix minimum")
    price_max   = models.FloatField(blank = True, null=True, verbose_name="Prix maximum")

    def __str__(self):
        return ''+self.producer
