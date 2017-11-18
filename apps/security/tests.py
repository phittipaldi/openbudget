from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import RegistrationForm


class UserFormTest(TestCase):

    # Valid Form Data
    def test_register_form_valid(self):
        form = RegistrationForm(data={'username': "user@mp.com",
                                      'full_name': "Tibaldi de Jesus",
                                      'password1': "tibaldix123",
                                      'password2': "tibaldix123", })
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_register_form_invalid(self):
        form = RegistrationForm(data={'username': "user@mp.com",
                                      'full_name': "Tibaldi de Jesus",
                                      'password1': "tibaldix123",
                                      'password2': "tibaldix", })
        self.assertFalse(form.is_valid())


class LoginRegisterTestCase(TestCase):

    def test_login(self):
        # First check for the default behavior
        response = self.client.get('/dashboard/')
        self.assertRedirects(response, '/accounts/login/?next=/dashboard/')

    # Redirect Form
    def test_redirects_after_POST(self):
        url = '/accounts/register/'
        response = self.client.post(url, data={'username': 'user@mp.com',
                                               'full_name': 'Tibaldi Jesus',
                                               'password1': 'tibaldix123',
                                               'password2': 'tibaldix123'})
        self.assertRedirects(response, '/accounts/verification_sent/')
