from django.contrib.auth.models import User


class PasswordlessAuthenticationBackend(object):

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
