from django.conf.urls import url
from .views import CurrencyRateView


urlpatterns = [
    url(r'^currency_rate/json/(?P<currency_pk>\d+)/$',
        CurrencyRateView.as_view(),
        name="currency_rate"),
]
