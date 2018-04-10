from django.contrib import admin
from django.contrib.auth.models import User
from . import models


@admin.register(models.BudgetShareStatus)
class BudgetShareStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BudgetShareMember)
class BudgetShareMemberAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BudgetYear)
class BudgetYearAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Budget)
class BudgetAdmin(admin.ModelAdmin):
    filter_horizontal = ('accounts', 'owners',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "accounts":
            kwargs["queryset"] = models.Account.objects.all_my_accounts(
                request.user)
        return super(BudgetAdmin,
                     self).formfield_for_manytomany(db_field,
                                                    request, **kwargs)


@admin.register(models.BudgetLine)
class BudgetLineAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PeriodType)
class PeriodTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BudgetPeriod)
class BudgetPeriodAdmin(admin.ModelAdmin):
    pass


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


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CurrencyUser)
class CurrencyUserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DurationFilter)
class DurationFilterAdmin(admin.ModelAdmin):
    pass


@admin.register(models.RecurrentTransaction)
class RecurrentAdmin(admin.ModelAdmin):
    pass


@admin.register(models.RecurrentShedule)
class RecurrentSheduleAdmin(admin.ModelAdmin):
    pass


@admin.register(models.RecurrentSheduleLine)
class RecurrentSheduleLineAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Bank)
class bankAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TemplateFile)
class TemplateFileAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FileType)
class FileTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FormatDate)
class FormatDateAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TransactionUploaded)
class TransactionUploadAdmin(admin.ModelAdmin):
    pass
