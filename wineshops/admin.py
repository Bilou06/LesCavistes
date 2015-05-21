from django.contrib import admin
from .models import Shop, Country, Region, Area, Color, Wine, Capacity


class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country')

admin.site.register(Shop, ShopAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_filter = ('custom',)

admin.site.register(Country, CountryAdmin)

class RegionAdmin(admin.ModelAdmin):
    list_filter = ('custom', 'country')
    list_display = ('name', 'country', 'custom')

admin.site.register(Region, RegionAdmin)

class AreaAdmin(admin.ModelAdmin):
    list_filter = ('custom', 'region')
    list_display = ('name', 'country', 'region', 'custom')

    def country(self, obj):
        return obj.region.country

admin.site.register(Area, AreaAdmin)

class ColorAdmin(admin.ModelAdmin):
    list_filter = ('custom', 'name',)

admin.site.register(Color, ColorAdmin)

class CapacityAdmin(admin.ModelAdmin):
    list_filter = ('custom', )
    list_display = ('custom', 'volume', )

admin.site.register(Capacity, CapacityAdmin)

class WineAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['shop', 'in_stock']}),
        ('Vin', {'fields': ['producer', 'country', 'region', 'area', 'color', 'classification', 'vintage', 'capacity', 'price_min', 'price_max']})
    ]

    list_display = ('shop', 'producer', 'country', 'region', 'area', 'color', 'classification', 'vintage', 'capacity', 'price_min', 'price_max', 'in_stock')

    list_per_page = 2

admin.site.register(Wine, WineAdmin)

