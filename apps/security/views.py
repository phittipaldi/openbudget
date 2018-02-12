# -*- encoding: utf-8 -*-
from django.views.generic.edit import FormView
from django.views.generic import RedirectView
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from .forms import RegistrationForm
from django.contrib.auth import views
from apps.utils.services import mail
from django.conf import settings


class UserActivation(FormView):
    template_name = 'security/activation.html'
    form_class = RegistrationForm


class UserRegistration(FormView):
    template_name = 'security/register.html'
    form_class = RegistrationForm

    def form_valid(self, form):
        form.instance.is_active = False
        form.save()
        # return super(UserRegistration, self).form_valid(form)
        self.send_notification(form.instance.email)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('accounts:verification_sent')

    def send_notification(self, email):
        subject = 'Formulario Solicitud Proyecto'
        html = render_to_string("security/mail/new_user.html", {
                                'current_domain': settings.CURRENT_DOMAIN})

        mail.send_html_mail(subject, html, [email])


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        views.logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


def verification_sent(request):
    return render_to_response('security/verification_sent.html')
