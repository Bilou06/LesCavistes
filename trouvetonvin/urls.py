from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [

    url(r'^user_profile/', include('user_profile.urls', namespace='user_profile')),
    url(r'^user/', include('user_profile.urls', namespace='user_profile')),
    url(r'^wineshops/', include('wineshops.urls', namespace='wineshops')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('wineshops.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)