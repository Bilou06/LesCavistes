__author__ = 'Sylvain'

from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /wineshops/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /wineshops/5/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /wineshops/edit/
    url(r'^edit/$', views.edit_user, name='edit'),
    url(r'^edit/user/$', views.edit_user, name='edit_user'),
    url(r'^edit/wineshop/$', views.edit_wineshop, name='edit_wineshop'),
    url(r'^edit/catalog/$', views.edit_catalog, name='edit_catalog'),
]
