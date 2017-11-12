from django.conf.urls import url
from django.contrib.auth import views
from .views import UserRegistration


urlpatterns = [
    url(r'^login/$', views.login,
        {'template_name': 'login.html'},
        name='login'),
    url(r'^register/$', UserRegistration.as_view(),
        name='register'),
]
