# -*- encoding: utf-8 -*-
from django import forms
from . import models


class AccountTransactionForm(forms.models.ModelForm):
    name = forms.CharField(required=True,
                           label="Account:",
                           max_length=64)

    class Meta:
        model = models.Account
        fields = ('name', 'account_type', 'starting_amount', 'currency')
