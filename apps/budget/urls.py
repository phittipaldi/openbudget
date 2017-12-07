from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^accounts/$', views.AccountList.as_view(), name='account_list'),
]
