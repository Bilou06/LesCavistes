__author__ = 'Sylvain'

from django.conf.urls import url

from . import views




urlpatterns = [
    # ex: /sign_up/
    url(r'^sign_up/$', views.register_user, name='register'),
    # ex: /register_success/
    url(r'^register_success/$', views.register_success, name='success'),
    # ex: /confirm/
    url(r'^confirm/(?P<activation_key>\w+)/$', views.register_confirm, name='new'),
    # ex: /resend_mail/
    url(r'^resend_mail/$', views.resend_mail, name='resend_mail'),
    # ex: /login/
    url(r'^login/$', views.login, name='login'),
]
