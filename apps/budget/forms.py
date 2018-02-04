# -*- encoding: utf-8 -*-
from django import forms
from django.forms import CheckboxSelectMultiple
from .models import (Account, AccountType,
                     Category, SubCategory, Transaction,
                     Budget, BudgetPeriod, PeriodType,
                     BudgetYear)
from apps.utils.models import Currency
import datetime


class BudgetForm(forms.models.ModelForm):

    class Meta:
        model = Budget
        fields = ('name', 'year', 'period_type', 'accounts')

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


class AccountTransactionForm(forms.models.ModelForm):

    class Meta:
        model = Account
        fields = ('name', 'account_type', 'starting_amount', 'currency')

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
        fields = ('name', 'account_type', 'starting_amount', 'currency')

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
