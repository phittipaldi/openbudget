# -*- coding: utf-8 -*-
from apps.budget.models import (IconCategory, Category, SubCategory,
                                AccountType, TransactionType, PeriodType)
from apps.utils.models import Color
from .users import create_super_user


def data_default_budget():

    user = create_super_user()
    AccountType.objects.get_or_create(name="Cash")
    AccountType.objects.get_or_create(name="General")

    TransactionType.objects.get_or_create(name="Expense")
    TransactionType.objects.get_or_create(name="Income")
    TransactionType.objects.get_or_create(name="Transfer")

    PeriodType.objects.get_or_create(name="Monthly", code="MONTHLY")

    red = Color.objects.get_or_create(name="Red")[0]
    blue = Color.objects.get_or_create(name="Blue")[0]
    green = Color.objects.get_or_create(name="Green")[0]
    gray = Color.objects.get_or_create(name="Gray")[0]

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

    icon_housing = IconCategory.objects.get_or_create(name="Housing",
                                                      color=blue,
                                                      css="pe-7s-home")

    icon_life = IconCategory.objects.get_or_create(name="Life & Entertainment",
                                                   color=green,
                                                   css="pe-7s-sun")

    icon_others = IconCategory.objects.get_or_create(name="Others",
                                                     color=gray,
                                                     css="pe-7s-keypad")

    food = Category.objects.get_or_create(name="Food & Drink",
                                          icon=icon_wine)[0]

    vehicle = Category.objects.get_or_create(name="Vehicle",
                                             icon=icon_car)[0]

    medicine = Category.objects.get_or_create(name="Medicine",
                                              icon=icon_medicine[0])[0]

    housing = Category.objects.get_or_create(name="Housing",
                                             icon=icon_housing[0])[0]

    life = Category.objects.get_or_create(name="Housing",
                                          icon=icon_life[0])[0]

    others = Category.objects.get_or_create(name="Others",
                                            icon=icon_others[0])[0]

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

    # --------HOUSING CATEGORY-----------------
    SubCategory.objects.get_or_create(category=housing,
                                      name="General - Housing",
                                      user_insert=user)

    SubCategory.objects.get_or_create(category=housing,
                                      name="Energy, utilities",
                                      user_insert=user)

    SubCategory.objects.get_or_create(category=housing,
                                      name="Maintenance, repairs",
                                      user_insert=user)

    SubCategory.objects.get_or_create(category=housing,
                                      name="Mortgage",
                                      user_insert=user)

    SubCategory.objects.get_or_create(category=housing,
                                      name="Rent",
                                      user_insert=user)

    SubCategory.objects.get_or_create(category=housing,
                                      name="Services",
                                      user_insert=user)

    # --------LIFE & ENTERTAINMENT CATEGORY-----------------
    SubCategory.objects.get_or_create(category=life,
                                      name="General - Life & Entertainment",
                                      user_insert=user)

    SubCategory.objects.get_or_create(category=life,
                                      name="Theater",
                                      user_insert=user)

    SubCategory.objects.get_or_create(category=life,
                                      name="Education, development",
                                      user_insert=user)

    # --------OTHERS CATEGORY-----------------
    SubCategory.objects.get_or_create(category=others,
                                      name="General - Others",
                                      user_insert=user)
