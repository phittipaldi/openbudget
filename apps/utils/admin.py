from django.contrib import admin
from . import models


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Color)
class ColorAdmin(admin.ModelAdmin):
    pass
