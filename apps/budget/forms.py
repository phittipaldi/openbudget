# -*- encoding: utf-8 -*-
from django import forms
from .models import Account, AccountType
from apps.utils.models import Currency


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
