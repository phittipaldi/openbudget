# # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.response import Response
from rest_framework.views import APIView
from apps.budget import models
from rest_framework.authentication import (SessionAuthentication,
                                           BasicAuthentication
                                           )


class DataBudget(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = []

    def get(self, request, **kwargs):
        queryset = self.filter_data(kwargs)
        labels = self.set_labels(queryset)
        default_items = self.set_defaults(queryset)
        bg_colors = self.set_bg_colors(queryset)
        ln_colors = self.set_ln_colors(queryset)
        data = {
            "labels": labels,
            "default": default_items,
            "bg_colors": bg_colors,
            "ln_colors": ln_colors
        }

        return Response(data)

    def set_labels(self, queryset):
        labels = []
        for item in queryset:
            labels.append(item.restaurant.name)

        return labels

    def set_defaults(self, queryset):
        default_items = []
        for item in queryset:
            default_items.append(item.rating)

        return default_items

    def filter_data(self, kwargs):
        queryset = models.RestaurantResult.objects.filter(
            restaurant__is_active=True,
            period__pk=kwargs['period']).order_by('rating')

        return queryset

    def set_bg_colors(self, queryset):
        bg_colors = []
        for item in queryset:
            bg_colors.append(item.restaurant.color.bg_code)

        return bg_colors

    def set_ln_colors(self, queryset):
        ln_colors = []
        for item in queryset:
            ln_colors.append(item.restaurant.color.border_code)

        return ln_colors