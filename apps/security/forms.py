# -*- encoding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from apps.security.models import ActivationPending
from django import forms
from django.contrib.auth import authenticate
from django import forms


class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(required=True,
                                label="First name:",
                                max_length=100)

    class Meta:
        model = User
        fields = ('first_name', 'email', 'username', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)

        user.email = self.cleaned_data['username']
        user.first_name = self.cleaned_data['full_name']
        if commit:
            user.save()
        return user


class ActivationForm(forms.models.ModelForm):
    # token = forms.CharField(required=True,
    #                         label="Token",
    #                         max_length=100)

    class Meta:
        model = ActivationPending
        fields = ('user', 'token')
        widgets = {'user': forms.HiddenInput(attrs={'required': False}),
                   'token': forms.HiddenInput(attrs={'required': False})}
