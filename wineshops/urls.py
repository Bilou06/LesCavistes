__author__ = 'Sylvain'

from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /wineshops/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /wineshops/5/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /wineshops/edit/
    url(r'^new/$', views.edit, name='edit'),
]
