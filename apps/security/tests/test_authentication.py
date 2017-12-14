from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.security.authentication import PasswordlessAuthenticationBackend
User = get_user_model()


class GetUserTest(TestCase):

    def test_gets_user_by_email(self):
        import ipdb; ipdb.set_trace()
        User.objects.create(email='another@example.com')
        desired_user = User.objects.create(email='edith@example.com')
        found_user = PasswordlessAuthenticationBackend().get_user(
            'edith@example.com'
        )
        self.assertEqual(found_user, desired_user)
