from dateutil.relativedelta import relativedelta
import calendar


class RecurrentSheduleService(object):

    def set_next_shedule_line(self):
        if self.day.period_type.code == 'MONTHLY':
            self.set_shedule_monthly()

    def set_shedule_monthly(self):

        if self.lines.count() == 0:
            self.lines.create(
                et_date=self.start_posting
            )
        else:
            last_shedule_line = self.lines.all().last()

            next_date = last_shedule_line.et_date + (
                relativedelta(months=1))

            next_date = self.replace_day(next_date)

            self.lines.create(
                et_date=next_date)

    def replace_day(self, next_date):

        try:
            next_date = next_date.replace(
                day=int(self.day.value))
        except Exception:
            last_day = self.get_last_day(next_date)
            next_date = next_date.replace(
                day=last_day)

        return next_date

    def get_last_day(self, next_date):

        result = calendar.monthrange(
            next_date.year,
            next_date.month)[1]
        return result
