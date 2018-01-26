from django.conf.urls import url
from django.contrib.auth import views
from . import views as core

urlpatterns = [
    url(r'^login/$', views.login,
        {'template_name': 'security/login.html'},
        name='login'),
    url(r'^logout/$', views.logout,
        {'template_name': 'security/login.html'},
        name='logout'),
    url(r'^register/$', core.UserRegistration.as_view(),
        name='register'),
    url(r'^verification_sent/$', core.verification_sent,
        name='verification_sent'),
]
