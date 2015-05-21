from django.contrib import admin

# Register your models here.
from user_profile.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
        fieldsets = [
        (None,  {'fields': ['user']}),
        ('Facturation', {'fields': ['name', 'address', 'city', 'zip_code', 'VAT']})
    ]


admin.site.register(UserProfile, UserProfileAdmin)