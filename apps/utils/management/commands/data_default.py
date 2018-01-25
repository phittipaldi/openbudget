# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from apps.utils import initial_data


class Command(BaseCommand):
    def handle(self, *args, **options):
        initial_data.users.create_super_user()
        initial_data.utils.data_default_utils()
        initial_data.budget.data_default_budget()
