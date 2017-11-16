# -*- encoding: utf-8 -*-
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from .forms import RegistrationForm


class UserRegistration(FormView):
    template_name = 'register.html'
    form_class = RegistrationForm

    def form_valid(self, form):
        form.save()
        # return super(UserRegistration, self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('security:account_activation_sent')


def account_activation_sent(request):
    return render_to_response('home.html')
    # return render_to_response('account_activation_sent.html')
