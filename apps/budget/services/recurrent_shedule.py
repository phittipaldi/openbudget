from dateutil.relativedelta import relativedelta


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
            last_shedule_line = self.lines.all()[-1]
            next_date = last_shedule_line.et_date + (
                relativedelta(months=1))
            self.shedule_lines.create(
                et_date=next_date)
