from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [

    url(r'^user_profile/', include('user_profile.urls', namespace='user_profile')),
    url(r'^user/', include('user_profile.urls', namespace='user_profile')),
    url(r'^wineshops/', include('wineshops.urls', namespace='wineshops')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('wineshops.urls')),
]
