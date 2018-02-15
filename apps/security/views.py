# -*- encoding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.views.generic.edit import FormView
from django.views.generic import RedirectView
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from .forms import RegistrationForm, ActivationForm
from django.contrib.auth import views
from apps.utils.services import mail
from .models import ActivationPending


class UserActivation(FormView):
    template_name = 'security/activation.html'
    form_class = ActivationForm

    def get_context_data(self, **kwargs):
        context = super(UserActivation, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.POST['user'])
        user.is_active = True
        user.save()
        login(request, user,
              backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('dashboard')

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def get_initial(self):
        pending = ActivationPending.objects.get(
            token=self.kwargs.get('token'))
        return {'user': pending.user, 'token': pending.token}


class UserRegistration(FormView):
    template_name = 'security/register.html'
    form_class = RegistrationForm

    def form_valid(self, form):
        form.instance.is_active = False
        form.save()
        # return super(UserRegistration, self).form_valid(form)
        pending_activation = self.create_pending_activation(form.instance)
        self.send_notification(pending_activation)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('verification_sent')

    def send_notification(self, pending_activation):
        subject = 'Formulario Solicitud Proyecto'
        html = render_to_string("security/mail/new_user.html", {
                                'current_domain': settings.CURRENT_DOMAIN,
                                'token': pending_activation.token})

        mail.send_html_mail(subject, html, [pending_activation.user.email])

    def create_pending_activation(self, user):
        expiration = datetime.today() + timedelta(days=30)
        result = ActivationPending.objects.create(
            user=user,
            expiration_date=expiration)
        return result


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
