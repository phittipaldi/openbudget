import datetime
from decimal import Decimal
import pytz


class TransactionFileService(object):

    def __init__(self):
        from .. import models
        self.model = models

    def import_file(self, file, account, user_insert):

        if self.file_type.extention == 'txt':
            self.process_txt(file, account, user_insert)

    def process_txt(self, file, account, user_insert):
        for line in file:
            try:
                fields = line.split(self.split_char)
                date_v = self.set_date(fields[self.field_pos_date])
                amount_v = self.set_amount(fields[self.field_pos_amount])
                descrip_v = fields[self.field_pos_description]
                reference_v = fields[self.field_pos_reference]
                subcategory = self.set_category(descrip_v, user_insert)
                trx_type_v = self.set_trx_type(
                    fields[self.field_pos_trans_type])

                if trx_type_v.name == "Expense":

                    self.model.TransactionUploaded.objects.get_or_create(
                        account=account,
                        description=descrip_v,
                        reference=reference_v,
                        amount=amount_v,
                        date=date_v,
                        trx_type=trx_type_v,
                        subcategory=subcategory,
                        user_insert=user_insert
                    )
            except Exception as e:
                print(e)

    def set_date(self, date_value):

        data = date_value.split(self.format_date.split_char)

        if self.format_date.has_year:
            year = int(data[self.format_date.pos_year])
        else:
            year = datetime.date.today().year

        month = int(data[self.format_date.pos_month])
        day = int(data[self.format_date.pos_day])
        value = datetime.datetime(year, month, day, 20, 8, 7, 127325,
                                  tzinfo=pytz.UTC)

        return value

    def set_amount(self, amount_value):
        try:
            value = Decimal(amount_value)
        except Exception:
            value = Decimal(amount_value[2:])
        return value

    def set_trx_type(self, trx_type_value):

        if trx_type_value == self.spend_char:
            value = self.model.TransactionType.objects.get(
                name="Expense")
        elif trx_type_value == self.income_char:
            value = self.model.TransactionType.objects.get(
                name="Income")
        else:
            value = self.model.TransactionType.objects.get(
                name="Transfer")

        return value

    def set_category(self, description, user_insert):

        categories = self.model.SubcategoryByDescription.objects.filter(
            description=description,
            user_insert=user_insert
        )
        if categories:
            category = categories.last().subcategory
        else:
            category = self.model.SubCategory.objects.get(
                name='General - Others',
                category__user_insert=user_insert)

        return category
