# -*- coding: utf-8 -*-
from apps.budget.models import (IconCategory, Category, SubCategory,
                                AccountType, TransactionType, PeriodType,
                                DurationFilter, DayShedule, Bank, TemplateFile,
                                FormatDate, FileType)
from apps.utils.models import Color
from .users import create_super_user


def data_default_budget():

    user = create_super_user()
    AccountType.objects.get_or_create(name="Cash")
    AccountType.objects.get_or_create(name="General")

    TransactionType.objects.get_or_create(name="Expense")
    TransactionType.objects.get_or_create(name="Income")
    TransactionType.objects.get_or_create(name="Transfer")

    monthly = PeriodType.objects.get_or_create(name="Monthly", code="MONTHLY")[0]

    DurationFilter.objects.get_or_create(name="Last 30 days", value=30,
                                         is_day=True)

    DurationFilter.objects.get_or_create(name="Past 3 months", value=3,
                                         is_month=True)

    DurationFilter.objects.get_or_create(name="Past 6 months", value=6,
                                         is_month=True)

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
                                          icon=icon_wine,
                                          user_insert=user)[0]

    vehicle = Category.objects.get_or_create(name="Vehicle",
                                             icon=icon_car,
                                             user_insert=user)[0]

    medicine = Category.objects.get_or_create(name="Medicine",
                                              icon=icon_medicine[0],
                                              user_insert=user)[0]

    housing = Category.objects.get_or_create(name="Housing",
                                             icon=icon_housing[0],
                                             user_insert=user)[0]

    life = Category.objects.get_or_create(name="Life & Entertainment",
                                          icon=icon_life[0],
                                          user_insert=user)[0]

    others = Category.objects.get_or_create(name="Others",
                                            icon=icon_others[0],
                                            user_insert=user)[0]

    SubCategory.objects.get_or_create(category=food,
                                      name="General - Food & Drink")

    SubCategory.objects.get_or_create(category=food,
                                      name="Bar, cafe")

    SubCategory.objects.get_or_create(category=food,
                                      name="Groceries")

    SubCategory.objects.get_or_create(category=food,
                                      name="Restaurant, fast-food")

    # --------VEHICULE CATEGORY----------------
    SubCategory.objects.get_or_create(category=vehicle,
                                      name="General - Vehicle")

    SubCategory.objects.get_or_create(category=vehicle,
                                      name="Fuel")

    SubCategory.objects.get_or_create(category=vehicle,
                                      name="Leasing")

    SubCategory.objects.get_or_create(category=vehicle,
                                      name="Parking")

    SubCategory.objects.get_or_create(category=vehicle,
                                      name="Rentals")

    SubCategory.objects.get_or_create(category=vehicle,
                                      name="Vehicle Insurance")

    SubCategory.objects.get_or_create(category=vehicle,
                                      name="Vehicle Maintanance")

    SubCategory.objects.get_or_create(category=vehicle,
                                      name="Vehicle Maintanance")

    # --------MEDICINE CATEGORY----------------

    SubCategory.objects.get_or_create(category=medicine,
                                      name="Health Care, doctor")

    SubCategory.objects.get_or_create(category=medicine,
                                      name="Drug-store, chemist")

    # --------HOUSING CATEGORY-----------------
    SubCategory.objects.get_or_create(category=housing,
                                      name="General - Housing")

    SubCategory.objects.get_or_create(category=housing,
                                      name="Energy, utilities")

    SubCategory.objects.get_or_create(category=housing,
                                      name="Maintenance, repairs")

    SubCategory.objects.get_or_create(category=housing,
                                      name="Mortgage")

    SubCategory.objects.get_or_create(category=housing,
                                      name="Rent")

    SubCategory.objects.get_or_create(category=housing,
                                      name="Services")

    # --------LIFE & ENTERTAINMENT CATEGORY-----------------
    SubCategory.objects.get_or_create(category=life,
                                      name="General - Life & Entertainment")

    SubCategory.objects.get_or_create(category=life,
                                      name="Theater")

    SubCategory.objects.get_or_create(category=life,
                                      name="Education, development")

    # --------OTHERS CATEGORY-----------------
    SubCategory.objects.get_or_create(category=others,
                                      name="General - Others")

    # --------RECURRENT DAY SHEDULE---------------------
    DayShedule.objects.get_or_create(period_type=monthly,
                                     name='First',
                                     value=1)

    DayShedule.objects.get_or_create(period_type=monthly,
                                     name='Last',
                                     value='last')

    DayShedule.objects.get_or_create(period_type=monthly,
                                     name='2nd',
                                     value=2)

    DayShedule.objects.get_or_create(period_type=monthly,
                                     name='3rd',
                                     value=3)

    DayShedule.objects.get_or_create(period_type=monthly,
                                     name='4th',
                                     value=4)

    DayShedule.objects.get_or_create(period_type=monthly,
                                     name='5th',
                                     value=5)

    DayShedule.objects.get_or_create(period_type=monthly,
                                     name='10th',
                                     value=10)

    DayShedule.objects.get_or_create(period_type=monthly,
                                     name='15th',
                                     value=15)

    DayShedule.objects.get_or_create(period_type=monthly,
                                     name='20th',
                                     value=20)

    DayShedule.objects.get_or_create(period_type=monthly,
                                     name='25th',
                                     value=25)

    DayShedule.objects.get_or_create(period_type=monthly,
                                     name='30th',
                                     value=30)

    # --------------TEMPLATE BANKING ACCOUNT ---------------------
    bank = Bank.objects.get_or_create(name='Banco Popular Dominicano',
                                      country='Dominican Republic',
                                      is_active=True,
                                      user_insert=user)[0]

    fdate = FormatDate.objects.get_or_create(name='ddmm',
                                             pos_day=0,
                                             pos_month=1,
                                             pos_year=2,
                                             split_char='/')[0]

    file_type = FileType.objects.get_or_create(name='Text File',
                                               extention='txt')[0]

    TemplateFile.objects.get_or_create(bank=bank,
                                       field_pos_date=1,
                                       field_pos_amount=3,
                                       field_pos_description=5,
                                       field_pos_trans_type=4,
                                       format_date=fdate,
                                       file_type=file_type,
                                       spend_char='CR',
                                       income_char='DB',
                                       split_char=','
                                       )
