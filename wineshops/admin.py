from django.contrib import admin
from .models import Shop, Country, Region, Area, Color, Wine


class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country')

admin.site.register(Shop, ShopAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_filter = ('custom',)

admin.site.register(Country, CountryAdmin)

class RegionAdmin(admin.ModelAdmin):
    list_filter = ('custom',)

admin.site.register(Region, RegionAdmin)

class AreaAdmin(admin.ModelAdmin):
    list_filter = ('custom',)

admin.site.register(Area, AreaAdmin)
admin.site.register(Color)


class WineAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['shop']}),
        ('Vin', {'fields': ['producer', 'country', 'region', 'area', 'color', 'classification', 'vintage', 'capacity', 'price_min', 'price_max']})
    ]

    list_display = ('shop', 'producer', 'country', 'region', 'area', 'color', 'classification', 'vintage', 'capacity', 'price_min', 'price_max')

    list_per_page = 2

admin.site.register(Wine, WineAdmin)

