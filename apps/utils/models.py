from django.db import models
from django.contrib.auth.models import User


class CommonInfo(models.Model):
    user_insert = models.ForeignKey(
        User,
        related_name='user_insert_%(class)s',
        editable=False)
    user_update = models.ForeignKey(
        User,
        related_name='user_update_%(class)s',
        blank=True, null=True, editable=False)

    class Meta:
        abstract = True


class Color(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
