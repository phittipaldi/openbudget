from django.contrib import admin
from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ActivationPending)
class ActivationAdmin(admin.ModelAdmin):
    pass
