from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand
from apps.security.tests.factories import UserFactory


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('username')

    def handle(self, *args, **options):
        session_key = create_authenticated_session(options['username'])
        self.stdout.write(session_key)


def create_authenticated_session(username):
    user = UserFactory(username=username)
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    return session.session_key
