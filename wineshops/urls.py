__author__ = 'Sylvain'

from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /wineshops/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /wineshops/edit/
    url(r'^edit/$', views.edit_user, name='edit'),
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
]
