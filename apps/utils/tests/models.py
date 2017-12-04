from django.test import TestCase
from .models import Color, Currency


class ModelTest(TestCase):

    def test_color(self):
        color = Color.objects.create(name='blue')

        self.assertEqual(color.__str__(), 'blue')

    def test_currency(self):
        currency = Currency.objects.create(name='USD')

        self.assertEqual(currency.__str__(), 'USD')
