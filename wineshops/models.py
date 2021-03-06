# -*- coding: utf-8 -*-
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit, Transpose
from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'user_{0}/{1}'.format(instance.user.id, filename)

# due to limitations in makemigrations, I must declare each function in the body
def user_directory_path_ldpi(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<dpi>/<filename>
        return 'user_{0}/ldpi/{1}'.format(instance.user.id, filename)

def user_directory_path_mdpi(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<dpi>/<filename>
        return 'user_{0}/mdpi/{1}'.format(instance.user.id, filename)

def user_directory_path_mdpi(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<dpi>/<filename>
        return 'user_{0}/mdpi/{1}'.format(instance.user.id, filename)

def user_directory_path_hdpi(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<dpi>/<filename>
        return 'user_{0}/hdpi/{1}'.format(instance.user.id, filename)

def user_directory_path_xhdpi(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<dpi>/<filename>
        return 'user_{0}/xhdpi/{1}'.format(instance.user.id, filename)


class Shop(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom du magasin", null=True)
    address = models.CharField(max_length=250, verbose_name="Adresse", null=True)
    city = models.CharField(max_length=100, verbose_name="Ville", null=True)
    zip_code = models.IntegerField(verbose_name="Code postal", null=True)
    country = models.CharField(max_length=100, default='France', verbose_name="Pays")
    description = models.TextField(max_length=500, blank=True, verbose_name="Description", null=True)
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone", null=True)
    mail = models.EmailField(blank=True, verbose_name="E-mail", null=True)
    web = models.CharField(max_length=50, blank=True, verbose_name="Site web", null=True)
    user = models.ForeignKey(User)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    filled = models.BooleanField(default=False)

    image = ProcessedImageField(upload_to=user_directory_path,
                                default='media/None/default.png',
                                processors=[Transpose(), ResizeToFit(height=100, width=100, upscale=False)],
                                format='JPEG',
                                options={'quality': 60},
                                verbose_name='Image', blank=True, null=True)

    image_ldpi = ProcessedImageField(upload_to=user_directory_path_ldpi,
                                     default='media/None/default.png',
                                     processors=[Transpose(), ResizeToFit(height=75, width=75, upscale=False)],
                                     format='JPEG',
                                     options={'quality': 60},
                                     verbose_name='Image', blank=True, null=True)

    image_mdpi = ProcessedImageField(upload_to=user_directory_path_mdpi,
                                     default='media/None/default.png',
                                     processors=[Transpose(), ResizeToFit(height=100, width=100, upscale=False)],
                                     format='JPEG',
                                     options={'quality': 60},
                                     verbose_name='Image', blank=True, null=True)

    image_hdpi = ProcessedImageField(upload_to=user_directory_path_hdpi,
                                     default='media/None/default.png',
                                     processors=[Transpose(), ResizeToFit(height=150, width=150, upscale=False)],
                                     format='JPEG',
                                     options={'quality': 60},
                                     verbose_name='Image', blank=True, null=True)

    image_xhdpi = ProcessedImageField(upload_to=user_directory_path_xhdpi,
                                      default='media/None/default.png',
                                      processors=[Transpose(), ResizeToFit(height=200, width=200, upscale=False)],
                                      format='JPEG',
                                      options={'quality': 60},
                                      verbose_name='Image', blank=True, null=True)

    def __str__(self):
        if self.name:
            return self.name
        return ''


class Country(models.Model):  # France, ...
    name = models.CharField(max_length=50, unique=True)
    custom = models.BooleanField(default=False)  # custom = False -> appear in combo box for everyone

    def __str__(self):
        if self.name:
            return self.name
        else:
            return ""


class Region(models.Model):  # Bordeaux, ...
    country = models.ForeignKey(Country)
    name = models.CharField(max_length=50)
    custom = models.BooleanField(default=False)  # custom = False -> appear in combo box for everyone

    def __str__(self):
        if self.name:
            return self.name
        else:
            return ""


class Area(models.Model):  # Saint-estèphe ...
    region = models.ForeignKey(Region)
    name = models.CharField(max_length=50)
    custom = models.BooleanField(default=False)  # custom = False -> appear in combo box for everyone

    def __str__(self):
        if self.name:
            return self.name
        else:
            return ""


class Color(models.Model):
    name = models.CharField(max_length=20)
    custom = models.BooleanField(default=False)  # custom = False -> appear in combo box for everyone

    def __str__(self):
        return self.name


class Capacity(models.Model):
    volume = models.FloatField(default=75, verbose_name="Contenance", blank=True, null=True)
    custom = models.BooleanField(default=False)  # custom = False -> appear in combo box for everyone

    def value(self):
        if self.volume:
            return self.volume
        else:
            return 0

    def __str__(self):
        if self.volume:
            return str(self.volume)
        else:
            return ""


class Wine(models.Model):
    shop = models.ForeignKey(Shop)
    producer = models.CharField(max_length=50, blank=True, verbose_name="Producteur")
    country = models.ForeignKey(Country, verbose_name="Pays", blank=True, null=True)
    region = models.ForeignKey(Region, verbose_name="Vignoble", blank=True, null=True)
    area = models.ForeignKey(Area, verbose_name="Appellations", blank=True, null=True)
    vintage = models.IntegerField(blank=True, null=True, verbose_name="Millésime")
    classification = models.CharField(max_length=50, blank=True, verbose_name="Classification")
    color = models.ForeignKey(Color, verbose_name="Couleur", blank=True, null=True)
    varietal = models.CharField(max_length=250, blank=True, null=True, verbose_name="Cépage")
    capacity = models.ForeignKey(Capacity, verbose_name="Contenance", blank=True, null=True)
    price_min = models.FloatField(blank=True, null=True, verbose_name="Prix minimum")
    price_max = models.FloatField(blank=True, null=True, verbose_name="Prix maximum")
    in_stock = models.BooleanField(default=True, verbose_name="En stock")

    def __str__(self):
        return '' + self.producer
