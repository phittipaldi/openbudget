"""openbudget URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from apps.dashboard.views import DashboardPage, DashboardPageFilter
import debug_toolbar

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', DashboardPage.as_view(), name='home'),
    url(r'^dashboard/$', DashboardPage.as_view(), name='dashboard'),
    url(r'^dashboard/(?P<budget>\d+)/(?P<period>\d+)/$',
        DashboardPageFilter.as_view(), name='dashboard_filter'),
    url(r'^accounts/', include('apps.security.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^budget/', include('apps.budget.urls', namespace='budget')),
    url(r'^utils/', include('apps.utils.urls', namespace="utils")),
    url(r'^api/v1/', include('apps.api.urls', namespace='apiv1')),
    url(r'^__debug__/', include(debug_toolbar.urls)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    # import debug_toolbar
    # urlpatterns += [
    #     url(r'^__debug__/', include(debug_toolbar.urls)),
    # ] + urlpatterns
