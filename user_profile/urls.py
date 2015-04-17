__author__ = 'Sylvain'

from django.conf.urls import url

from . import views




urlpatterns = [
    url(r'^sign_up/$', views.register_user, name='register'),
    url(r'^register_success/$', views.register_success, name='success'),
    url(r'^confirm/(?P<activation_key>\w+)/$', views.register_confirm, name='new'),
    url(r'^resend_mail/$', views.resend_mail, name='resend_mail'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^change_password/$', views.password_change, name='change_password'),
    url(r'^forgotten_password/$', views.password_reset, name='forgotten_password'),
    url(r'^password_reset_done/$', views.password_reset_done, name='password_reset_done'),
    url(r'^password_reset_complete/$', views.password_reset_complete, name='password_reset_complete'),
    url(r'^contract/$', views.contract, name='contract'),
]
