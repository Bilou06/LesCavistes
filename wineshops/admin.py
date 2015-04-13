from django.contrib import admin
from .models import Shop, Country, Region, Area, Color, Wine


class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country')

admin.site.register(Shop, ShopAdmin)


admin.site.register(Country)
admin.site.register(Region)
admin.site.register(Area)
admin.site.register(Color)


class WineAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['shop']}),
        ('Vin', {'fields': ['producer', 'area', 'color', 'classification', 'vintage', 'capacity', 'price_min', 'price_max']})
    ]

    list_display = ('shop', 'producer', 'area', 'color', 'classification', 'vintage', 'capacity', 'price_min', 'price_max')

admin.site.register(Wine, WineAdmin)