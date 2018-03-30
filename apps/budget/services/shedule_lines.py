class SheduleLineService(object):

    def post_transaction(self):
        from apps.budget.models import Transaction

        Transaction.objects.create(
            account=self.shedule.recurrent_transaction.account,
            trx_type=self.shedule.recurrent_transaction.trx_type,
            subcategory=self.shedule.recurrent_transaction.subcategory,
            currency=self.shedule.recurrent_transaction.currency,
            amount=self.shedule.recurrent_transaction.amount,
            amount_account=self.shedule.recurrent_transaction.amount,
            exchange=1,
            place=self.shedule.recurrent_transaction.place,
            date=self.et_date,
            user_insert=self.shedule.recurrent_transaction.account.user_insert)
