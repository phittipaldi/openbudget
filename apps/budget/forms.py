# -*- encoding: utf-8 -*-
from django import forms
from django.forms import CheckboxSelectMultiple
from .models import (Account, AccountType,
                     Category, SubCategory, Transaction,
                     Budget, BudgetPeriod, PeriodType, DayShedule,
                     BudgetYear, CurrencyUser, BudgetShareMember,
                     RecurrentTransaction, RecurrentShedule, TemplateFile,
                     TransactionUploaded, Bank)
from apps.utils.models import Currency
import datetime


class CurrencyUserForm(forms.models.ModelForm):

    class Meta:
        model = CurrencyUser
        fields = ('currency', 'ratio', 'inverse_ratio', 'owner')
        widgets = {'owner': forms.HiddenInput(attrs={'required': False})}

    currency = forms.ModelChoiceField(
        queryset=Currency.objects.all().order_by('name'),
        empty_label="------------------",
        widget=forms.Select(attrs={'class': 'form-control'}))

    ratio = forms.CharField(required=True,
                            label="Ratio",
                            max_length=64,
                            widget=forms.TextInput(attrs={'class':
                                                          "form-control",
                                                          'placeholder':
                                                          'Ratio'}),)

    inverse_ratio = forms.CharField(required=True,
                                    label="Inverse Ratio",
                                    max_length=64,
                                    widget=forms.TextInput(
                                        attrs={'class': 'form-control',
                                               'placeholder': 'Ratio'}),)


class CurrencyUserUpdateForm(forms.models.ModelForm):

    class Meta:
        model = CurrencyUser
        fields = ('currency', 'ratio', 'inverse_ratio', 'owner')
        widgets = {'owner': forms.HiddenInput(attrs={'required': False})}

    currency = forms.ModelChoiceField(
        queryset=Currency.objects.all().order_by('name'),
        empty_label="------------------",
        widget=forms.Select(attrs={'class': 'form-control',
                                   'readonly': 'True'}))

    ratio = forms.CharField(required=True,
                            label="Ratio",
                            max_length=64,
                            widget=forms.TextInput(attrs={'class':
                                                          "form-control",
                                                          'placeholder':
                                                          'Ratio'}),)

    inverse_ratio = forms.CharField(required=True,
                                    label="Inverse Ratio",
                                    max_length=64,
                                    widget=forms.TextInput(
                                        attrs={'class': 'form-control',
                                               'placeholder': 'Ratio'}),)


class SubcategoryForm(forms.models.ModelForm):

    class Meta:
        model = SubCategory
        fields = ('name', 'category')
        widgets = {'category': forms.HiddenInput(attrs={'required': False})}

    name = forms.CharField(required=True,
                           label="Name",
                           widget=forms.TextInput(attrs={'class':
                                                         "form-control",
                                                         'placeholder':
                                                         "Subcategory Name"}))


class BudgetForm(forms.models.ModelForm):

    class Meta:
        model = Budget
        fields = ('name', 'year', 'period_type', 'currency', 'accounts')

    name = forms.CharField(required=True,
                           label="Name",
                           max_length=64,
                           widget=forms.TextInput(attrs={'class':
                                                         "form-control",
                                                         'placeholder':
                                                         'Budget name'}),)

    year = forms.ModelChoiceField(
        queryset=BudgetYear.objects.filter(is_active=True),
        empty_label="------------------",
        widget=forms.Select(attrs={'class': 'form-control'}))

    period_type = forms.ModelChoiceField(queryset=PeriodType.objects.all(),
                                         empty_label="------------------",
                                         widget=forms.Select(
                                         attrs={'class': 'form-control'}))

    currency = forms.ModelChoiceField(queryset=Currency.objects.all(),
                                      empty_label="------------------",
                                      widget=forms.Select(
                                      attrs={'class': 'form-control'}))

    accounts = forms.ModelMultipleChoiceField(queryset=Account.objects.all(),
                                              widget=CheckboxSelectMultiple,
                                              required=False, help_text='')


class BudgetReportForm(forms.Form):

    budget = forms.ModelChoiceField(queryset=Budget.objects.all(),
                                    empty_label="------------------",
                                    widget=forms.Select(
                                    attrs={'class': 'form-control'}))

    period = forms.ModelChoiceField(queryset=BudgetPeriod.objects.all(),
                                    empty_label="------------------",
                                    widget=forms.Select(
                                    attrs={'class': 'form-control'}))


class BudgetShareForm(forms.Form):

    budget = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Email'}))


class ImportTransactionForm(forms.Form):

    template_file = forms.ModelChoiceField(queryset=TemplateFile.objects.all(),
                                           empty_label="------------------",
                                           widget=forms.Select(
                                           attrs={'class': 'form-control'}))

    account = forms.IntegerField(widget=forms.HiddenInput())

    file = forms.FileField()


class UploadTransactionBaseForm(forms.ModelForm):

    class Meta:
        model = TransactionUploaded
        fields = ('subcategory',)


class UploadedTransactionForm(forms.models.ModelForm):

    category = forms.IntegerField()

    class Meta(UploadTransactionBaseForm.Meta):
        fields = ('category',) + UploadTransactionBaseForm.Meta.fields

    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label="------------------",
                                      widget=forms.Select(
                                      attrs={'class': 'form-control'}))

    subcategory = forms.ModelChoiceField(queryset=SubCategory.objects.all(),
                                         empty_label="------------------",
                                         widget=forms.Select(
                                         attrs={'class': 'form-control js-example-basic-single'}))


class ShareConfirmationForm(forms.models.ModelForm):

    class Meta:
        model = BudgetShareMember
        fields = ('status',)
        widgets = {'status': forms.HiddenInput(attrs={'required': False})}


class AccountTransactionForm(forms.models.ModelForm):

    class Meta:
        model = Account
        fields = ('name', 'account_type', 'bank',
                  'starting_amount', 'currency')

    name = forms.CharField(required=True,
                           label="Name",
                           max_length=64,
                           widget=forms.TextInput(attrs={'class':
                                                         "form-control",
                                                         'placeholder':
                                                         'Account name'}),)
    account_type = forms.ModelChoiceField(queryset=AccountType.objects.all(),
                                          empty_label="------------------",
                                          widget=forms.Select(
                                          attrs={'class': 'form-control'}))

    bank = forms.ModelChoiceField(queryset=Bank.objects.all(),
                                  empty_label="------------------",
                                  widget=forms.Select(
                                  attrs={'class': 'form-control'}),
                                  required=False)

    starting_amount = forms.CharField(required=True,
                                      label="Starting Amount",
                                      max_length=16,
                                      widget=forms.TextInput(attrs={'class':
                                                             'form-control'}
                                                             )
                                      )

    currency = forms.ModelChoiceField(queryset=Currency.objects.all(),
                                      empty_label="------------------",
                                      widget=forms.Select(
                                      attrs={'class': 'form-control'}))


class AccountTransactionUpdateForm(forms.models.ModelForm):

    class Meta:
        model = Account
        fields = ('name', 'account_type', 'bank',
                  'starting_amount', 'currency')

    name = forms.CharField(required=True,
                           label="Name",
                           max_length=64,
                           widget=forms.TextInput(attrs={'class':
                                                         "form-control",
                                                         'placeholder':
                                                         'Account name'}),)

    account_type = forms.ModelChoiceField(queryset=AccountType.objects.all(),
                                          empty_label="------------------",
                                          widget=forms.Select(
                                          attrs={'class': 'form-control'}))

    bank = forms.ModelChoiceField(queryset=Bank.objects.all(),
                                  empty_label="------------------",
                                  widget=forms.Select(
                                  attrs={'class': 'form-control'}),
                                  required=False)

    starting_amount = forms.CharField(required=True,
                                      label="Starting Amount",
                                      max_length=16,
                                      widget=forms.TextInput(attrs={'class':
                                                             'form-control',
                                                                    'readonly':
                                                                    'True'}
                                                             )
                                      )

    currency = forms.ModelChoiceField(queryset=Currency.objects.all(),
                                      empty_label="------------------",
                                      widget=forms.Select(attrs={'class':
                                                          'form-control',
                                                                 'readonly':
                                                                 'True'}
                                                          )
                                      )


class TransactionBaseForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('subcategory', 'account', 'amount', 'currency',
                  'place', 'date')


class TransactionForm(TransactionBaseForm):

    category = forms.IntegerField()

    class Meta(TransactionBaseForm.Meta):
        fields = ('account',
                  'category',) + TransactionBaseForm.Meta.fields

    account = forms.ModelChoiceField(queryset=Account.objects.all(),
                                     empty_label="------------------",
                                     widget=forms.Select(
                                     attrs={'class': 'form-control'}))

    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label="------------------",
                                      widget=forms.Select(
                                      attrs={'class': 'form-control'}))

    subcategory = forms.ModelChoiceField(queryset=SubCategory.objects.all(),
                                         empty_label="------------------",
                                         widget=forms.Select(
                                         attrs={'class': 'form-control'}))

    amount = forms.CharField(required=True,
                             label="Amount",
                             max_length=20,
                             widget=forms.TextInput(attrs={'class':
                                                    "form-control",
                                                           'placeholder':
                                                           "Amount"})
                             )

    currency = forms.ModelChoiceField(queryset=Currency.objects.all(),
                                      empty_label="------------------",
                                      widget=forms.Select(
                                      attrs={'class': 'form-control'}))

    place = forms.CharField(required=True,
                            label="Place",
                            max_length=128,
                            widget=forms.TextInput(attrs={'class':
                                                          "form-control",
                                                          'placeholder':
                                                          'Place Name'}),)

    date = forms.DateField(initial=datetime.date.today,
                           widget=forms.DateInput(attrs={'class':
                                                  "form-control datepicker",
                                                         'placeholder':
                                                         'Transaction Date'}),)

    def clean(self):
        amount = self.cleaned_data.get('amount').replace(',', '')
        self.cleaned_data['amount'] = amount


class RecurrentSheduleBaseForm(forms.ModelForm):

    class Meta:
        model = RecurrentShedule
        fields = ('day', 'start_posting')


class RecurrentSheduleForm(forms.models.ModelForm):

    period_type = forms.IntegerField()

    class Meta(RecurrentSheduleBaseForm.Meta):
        fields = ('period_type',) + RecurrentSheduleBaseForm.Meta.fields

    period_type = forms.ModelChoiceField(queryset=PeriodType.objects.all(),
                                         empty_label="------------------",
                                         widget=forms.Select(
                                         attrs={'class': 'form-control'}))

    day = forms.ModelChoiceField(queryset=DayShedule.objects.all(),
                                 empty_label="------------------",
                                 widget=forms.Select(
                                 attrs={'class': 'form-control'}))

    start_posting = forms.DateField(initial=datetime.date.today,
                                    widget=forms.DateInput(attrs={
                                        'class': 'form-control datepicker'}))


class RecurrentBaseForm(forms.ModelForm):

    class Meta:
        model = RecurrentTransaction
        fields = ('subcategory', 'account', 'amount', 'currency',
                  'place')


class RecurrentTransactionForm(forms.models.ModelForm):

    category = forms.IntegerField()

    class Meta(RecurrentBaseForm.Meta):
        fields = ('account', 'category',) + RecurrentBaseForm.Meta.fields

    account = forms.ModelChoiceField(queryset=Account.objects.all(),
                                     empty_label="------------------",
                                     widget=forms.Select(
                                     attrs={'class': 'form-control'}))

    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label="------------------",
                                      widget=forms.Select(
                                      attrs={'class': 'form-control'}))

    subcategory = forms.ModelChoiceField(queryset=SubCategory.objects.all(),
                                         empty_label="------------------",
                                         widget=forms.Select(
                                         attrs={'class': 'form-control'}))

    amount = forms.CharField(required=True,
                             label="Amount",
                             max_length=20,
                             widget=forms.TextInput(attrs={'class':
                                                    "form-control",
                                                           'placeholder':
                                                           "Amount mnk"})
                             )

    currency = forms.ModelChoiceField(queryset=Currency.objects.all(),
                                      empty_label="------------------",
                                      widget=forms.Select(
                                      attrs={'class': 'form-control'}))

    place = forms.CharField(required=True,
                            label="Place",
                            max_length=128,
                            widget=forms.TextInput(attrs={'class':
                                                          "form-control",
                                                          'placeholder':
                                                          'Place Name'}),)

    def clean(self):
        amount = self.cleaned_data.get('amount').replace(',', '')
        self.cleaned_data['amount'] = amount
