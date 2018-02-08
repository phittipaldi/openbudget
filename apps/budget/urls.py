from django.conf.urls import url
from . import views_account as views
from . import views_transaction as views_trx
from . import views_reports
from . import views_budget
from . import views_settings


urlpatterns = [
    url(r'^accounts/$', views.AccountList.as_view(), name='account_list'),
    url(r'^accounts/_add/$', views.AccountAdd.as_view(), name='account_add'),
    url(r'accounts/_update/(?P<pk>\d+)/$', views.AccountUpdate.as_view(),
        name='account_update'),
    url(r'accounts/_delete/(?P<pk>\d+)/$', views.AccountDelete.as_view(),
        name='account_delete'),

    url(r'^$', views_budget.BudgetList.as_view(),
        name='list'),
    url(r'^_create/$', views_budget.BudgetCreate.as_view(),
        name='create'),
    url(r'^_update/(?P<pk>\d+)/$', views_budget.BudgetUpdate.as_view(),
        name='update'),
    url(r'^_delete/(?P<pk>\d+)/$', views_budget.BudgetDelete.as_view(),
        name='delete'),
    url(r'^global_details/(?P<budget_pk>\d+)/$',
        views_budget.BudgetDetailGlobal.as_view(),
        name='budget_global_details'),
    url(r'^detail/(?P<pk>\d+)/$', views_budget.BudgetDetail.as_view(),
        name='detail'),

    url(r'transactions/$',
        views_trx.TransactionList.as_view(),
        name='transaction_list'),
    url(r'transactions/_filter/(?P<duration>\d+)/$',
        views_trx.TransactionList.as_view(),
        name='transaction_list_duration'),
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
    url(r'account/category/json/(?P<account_pk>\d+)/$',
        views_trx.CategoryView.as_view(),
        name='categories_x_account_user_insert'),

    url(r'^reports/$',
        views_reports.BudgetReport.as_view(),
        name='reports'),
    url(r'^reports/(?P<budget>\d+)/(?P<category>\d+)/(?P<period>\d+)/$',
        views_reports.BudgetbySubcategories.as_view(),
        name='report_subcategories'),
    url(r'^reports/details/(?P<subcategory>\d+)/(?P<period>\d+)/$',
        views_reports.TransactionDetails.as_view(),
        name='report_details'),
    url(r'^periods/json/(?P<budget>\d+)/$',
        views_reports.BudgetPeriodView.as_view(),
        name='budget_periods'),

    url(r'^setting/category/$',
        views_settings.SettingCategory.as_view(),
        name='setting_category'),
    url(r'^setting/subcategory/(?P<category_pk>\d+)/create/$',
        views_settings.SettingSubCategoryAdd.as_view(),
        name='setting_subcategory_add'),
    url(r'^setting/subcategory/(?P<pk>\d+)/update/$',
        views_settings.SettingSubCategoryUpdate.as_view(),
        name='setting_subcategory_update'),
    url(r'^setting/subcategory/(?P<pk>\d+)/delete/$',
        views_settings.SettingSubCategoryDelete.as_view(),
        name='setting_subcategory_delete'),

    url(r'^setting/currency/$',
        views_settings.SettingCurrency.as_view(),
        name='setting_currency')
]
