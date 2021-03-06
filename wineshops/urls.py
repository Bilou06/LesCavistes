__author__ = 'Sylvain'

from django.conf.urls import url
from django.conf.urls import handler404, handler500

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    # ex: /wineshops/
    url(r'^$', views.IndexView.as_view(), name='index'),
	
    # ex: /wineshops/edit/
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^edit/user/$', views.edit_user, name='edit_user'),
    url(r'^edit/wineshop/$', views.edit_wineshop, name='edit_wineshop'),
    url(r'^edit/catalog/$', views.edit_catalog, name='edit_catalog'),
    url(r'^edit/wine/(?P<wine_id>[0-9]+)/$', views.edit_wine, name='edit_wine'),
    url(r'^create/wine/$', views.create_wine.as_view(), name='create_wine'),
    url(r'^confirm_remove/(?P<wine_ids>[0-9]+(,[0-9]+)*)/$', views.confirm_remove, name="confirm_remove"),
    url(r'^search/$', views.search, name='search'),
    url(r'^regions/$', views.regions, name='regions'),
    url(r'^areas/$', views.areas, name='areas'),
    url(r'^in_wines/(?P<wine_ids>[0-9]+(,[0-9]+)*)$', views.in_wines, name='in_wines'),
    url(r'^out_wines/(?P<wine_ids>[0-9]+(,[0-9]+)*)$', views.out_wines, name='out_wines'),
    url(r'catalog/(?P<shop_id>[0-9]+)/$', views.filtered_catalog, name="filtered_catalog"),


    # for apps
    url(r'getwineshops/$', views.get_wine_shops, name="getwineshops"),
    url(r'getwines/$', views.get_wines, name="getwines"),
    url(r'getwineshopimage/(?P<shop_id>[0-9]+)/(?P<dpi>[a-z]+)/.*$', views.get_wineshop_image, name="getwineshopimage"),
]


handler404 = views.error404