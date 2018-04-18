from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^chart_data_budget/(?P<period>[^/]+)/$',
        views.DataBudget.as_view(),
        name='chart_data_budget'),
    url(r'^activity_data_budget/(?P<period>[^/]+)/$',
        views.DataBudgetActivity.as_view(),
        name='activity_data_budget')
]
