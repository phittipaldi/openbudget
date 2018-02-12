from django.db import models
from django.contrib.auth.models import User
from apps.budget.models import Category, SubCategory
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class ActivationPending(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True, max_length=32)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_pending = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        add_categories_default(instance)
    instance.profile.save()


def add_categories_default(user):

    categories_default = Category.objects.filter(
        user_insert__username='admin')

    for category in categories_default:

        category_created = Category.objects.get_or_create(name=category.name,
                                                          icon=category.icon,
                                                          user_insert=user)[0]

        for subcategory in category.subcategories.all():
            SubCategory.objects.get_or_create(category=category_created,
                                              name=subcategory.name)
