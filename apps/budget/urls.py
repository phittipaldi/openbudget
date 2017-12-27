from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^accounts/$', views.AccountList.as_view(), name='account_list'),
    url(r'^account/add/$', views.AccountAdd.as_view(), name='account_add'),
    url(r'account/update/(?P<pk>\d+)/$', views.AccountUpdate.as_view(),
        name='account_update'),
    url(r'account/delete/(?P<pk>\d+)/$', views.AccountDelete.as_view(),
        name='account_delete'),
]
