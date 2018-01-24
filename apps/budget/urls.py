from django.conf.urls import url
from . import views_account as views
from . import views_transaction as views_trx
from . import views_reports

urlpatterns = [
    url(r'^accounts/$', views.AccountList.as_view(), name='account_list'),
    url(r'^accounts/_add/$', views.AccountAdd.as_view(), name='account_add'),
    url(r'accounts/_update/(?P<pk>\d+)/$', views.AccountUpdate.as_view(),
        name='account_update'),
    url(r'accounts/_delete/(?P<pk>\d+)/$', views.AccountDelete.as_view(),
        name='account_delete'),

    url(r'transactions/$', views_trx.TransactionList.as_view(),
        name='transaction_list'),
    url(r'transactions/_add/$', views_trx.TransactionAdd.as_view(),
        name='transaction_add'),
    url(r'transactions/_update/(?P<pk>\d+)/$',
        views_trx.TransactionUpdate.as_view(),
        name='transaction_update'),
    url(r'transactions/_delete/(?P<pk>\d+)/$',
        views_trx.TransactionDelete.as_view(),
        name='transaction_delete'),

    url(r'category/subcategory/json/(?P<category>\d+)/$',
        views_trx.SubCategoryView.as_view(),
        name='subcategories_x_category'),

    url(r'^reports/$',
        views_reports.BudgetReport.as_view(),
        name='reports')
]
