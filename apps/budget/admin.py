from django.contrib import admin
from django.contrib.auth.models import User
from . import models


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    filter_horizontal = ('owners',)


@admin.register(models.AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        if instance.pk:
            instance.user_update = User.objects.get(
                username=request.user.username)
        else:
            instance.user_insert = User.objects.get(
                username=request.user.username)
        instance.save()
        return instance


@admin.register(models.IconCategory)
class IconCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CurrencyUser)
class CurrencyUserAdmin(admin.ModelAdmin):
    pass
