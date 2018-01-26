# -*- coding: utf-8 -*-
from apps.budget.models import (IconCategory, Category, SubCategory,
                                AccountType)
from apps.utils.models import Color
from .users import create_super_user


def data_default_budget():

    user = create_super_user()
    AccountType.objects.get_or_create(name="Cash")
    AccountType.objects.get_or_create(name="General")

    red = Color.objects.get_or_create(name="Red")[0]
    blue = Color.objects.get_or_create(name="Blue")[0]

    icon_wine = IconCategory.objects.get_or_create(name="Wine",
                                                   color=red,
                                                   css="pe-7s-wine")[0]

    icon_car = IconCategory.objects.get_or_create(name="Car",
                                                  color=blue,
                                                  css="pe-7s-car")[0]

    icon_medicine = IconCategory.objects.get_or_create(name="Medicine",
                                                       color=blue,
                                                       css="pe-7s-eyedropper")

    icon_medicine = IconCategory.objects.get_or_create(name="Medicine",
                                                       color=blue,
                                                       css="pe-7s-eyedropper")

    food = Category.objects.get_or_create(name="Food & Drink",
                                          icon=icon_wine)[0]

    vehicle = Category.objects.get_or_create(name="Vehicle",
                                             icon=icon_car)[0]

    medicine = Category.objects.get_or_create(name="Medicine",
                                              icon=icon_medicine[0])[0]

    SubCategory.objects.get_or_create(category=food,
                                      name="General - Food & Drink",
                                      user_insert=user)

    SubCategory.objects.get_or_create(category=food,
                                      name="Bar, cafe",
                                      user_insert=user)

    SubCategory.objects.get_or_create(category=food,
                                      name="Groceries",
                                      user_insert=user)

    SubCategory.objects.get_or_create(category=food,
                                      name="Restaurant, fast-food",
                                      user_insert=user)

    # --------VEHICULE CATEGORY----------------
    SubCategory.objects.get_or_create(category=vehicle,
                                      name="General - Vehicle",
                                      user_insert=user)

    SubCategory.objects.get_or_create(category=vehicle,
                                      name="Fuel",
                                      user_insert=user)

    SubCategory.objects.get_or_create(category=vehicle,
                                      name="Leasing",
                                      user_insert=user)

    SubCategory.objects.get_or_create(category=vehicle,
                                      name="Parking",
                                      user_insert=user)

    SubCategory.objects.get_or_create(category=vehicle,
                                      name="Rentals",
                                      user_insert=user)

    SubCategory.objects.get_or_create(category=vehicle,
                                      name="Vehicle Insurance",
                                      user_insert=user)

    SubCategory.objects.get_or_create(category=vehicle,
                                      name="Vehicle Maintanance",
                                      user_insert=user)

    SubCategory.objects.get_or_create(category=vehicle,
                                      name="Vehicle Maintanance",
                                      user_insert=user)

    # --------MEDICINE CATEGORY----------------

    SubCategory.objects.get_or_create(category=medicine,
                                      name="Health Care, doctor",
                                      user_insert=user)

    SubCategory.objects.get_or_create(category=medicine,
                                      name="Drug-store, chemist",
                                      user_insert=user)
