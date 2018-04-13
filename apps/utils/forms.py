# -*- coding: utf-8 -*-
from django import forms


class DatePickerField(forms.DateInput):
    class Media:
        js = ['js/utils/datepickerfield.js']


class SearchForm(forms.Form):
    pages = [(5, 5), (10, 10), (25, 25), (50, 50), (100, 100)]
    pb = forms.ChoiceField(
        required=False,
        choices=pages,
        widget=forms.Select(
            attrs={'class': 'input-sm'}))
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control search-list input-sm',
                   'placeholder': 'Search'})
    )

    class Media:
        js = ['js/utils/search_list.js']
