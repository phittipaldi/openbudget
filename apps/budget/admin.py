from django.contrib import admin
from . import models


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    pass
