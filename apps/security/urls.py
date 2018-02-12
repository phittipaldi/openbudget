from django.conf.urls import url
from django.contrib.auth import views
from . import views as core

urlpatterns = [
    url(r'^login/$', views.login,
        {'template_name': 'security/login.html'},
        name='login'),
    url(r'^logout/$', core.LogoutView.as_view(),
        name='logout'),
    url(r'^register/$', core.UserRegistration.as_view(),
        name='register'),
    url(r'^verification_sent/$', core.verification_sent,
        name='verification_sent'),
    url(r'^activation/(?P<token>[0-9a-f-]+)/$', core.UserActivation.as_view(),
        name='user_activation')
]
