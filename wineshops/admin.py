from django.contrib import admin
from .models import Shop, Country, Region, Area, Color, Wine

# Register your models here.

class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country')

admin.site.register(Shop, ShopAdmin)


admin.site.register(Country)
admin.site.register(Region)
admin.site.register(Area)
admin.site.register(Color)


class WineAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields' : ['shop']}),
        ('Vin', {'fields' : ['producer', 'area', 'color', 'classification', 'vintage', 'capacity']})
    ]

    list_display = ('shop', 'producer', 'area', 'color', 'classification', 'vintage', 'capacity')

admin.site.register(Wine, WineAdmin)