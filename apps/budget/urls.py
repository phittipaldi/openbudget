from django.conf.urls import url
from . import views_account as views
from . import views_transaction as views_trx

urlpatterns = [
    url(r'^accounts/$', views.AccountList.as_view(), name='account_list'),
    url(r'^account/add/$', views.AccountAdd.as_view(), name='account_add'),
    url(r'account/update/(?P<pk>\d+)/$', views.AccountUpdate.as_view(),
        name='account_update'),
    url(r'account/delete/(?P<pk>\d+)/$', views.AccountDelete.as_view(),
        name='account_delete'),

    url(r'transactions/$', views_trx.TransactionList.as_view(),
        name='transaction_list')
]
