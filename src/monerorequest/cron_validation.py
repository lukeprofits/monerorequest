import re

class CronValidation():
    delimiters = ',-/'
    month_codes = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    dow_codes = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    day_special = ['L']
    def __init__(self, schedule):
        self.schedule = schedule
        cron_def = self.parse_cron()
        self.minutes = cron_def['minutes']
        self.hours = cron_def['hours']
        self.days = cron_def['days']
        self.months = cron_def['months']
        self.dow = cron_def['dow']
        self.any = ['*']
        self.errors = []

    def parse_cron(self):
        schedule_args = self.schedule.split(' ')

        if len(schedule_args) < 5:
            raise ValueError('Invalid Cron: Too Few Of Arguments')

        sched = {}

        sched['minutes'] = re.split(self.delimiters, schedule_args[0])
        sched['hours'] = re.split(self.delimiters, schedule_args[1])
        sched['days'] = re.split(self.delimiters, schedule_args[2])
        sched['months'] = re.split(self.delimiters, schedule_args[3])
        sched['dow'] = re.split(self.delimiters, schedule_args[4])

        return sched

    def valid(self):
        if not self.valid_minutes():
            self.errors.append('Invalid Minutes')

        if not self.valid_hours():
            self.errors.append('Invalid Hours')

        if not self.valid_days():
            self.errors.append('Invalid Day')

        if not self.valid_months():
            self.errors.append('Invalid Month')

        if not self.valid_dow():
            self.errors.append('Invalid Day of the Week')

        if self.errors:
            return False
        else:
            return True

    def valid_minutes(self):
        if self.minutes == self.any:
            return True
        try:
            results = []
            for minute in self.minutes:
                int_minute = int(minute)
                results.append(int_minute >= 0 and int_minute <= 59)
            return any(results)
        except ValueError:
            return False

    def valid_hours(self):
        if self.hours == self.any:
            return True
        try:
            results = []
            for hour in self.hours:
                int_hour = int(hour)
                results.append(int_hour >= 0 and int_hour <= 23)
            return any(results)
        except ValueError:
            return False

    def valid_days(self):
        if self.days == self.any or self.days == self.day_special:
            return True
        try:
            results = []
            for day in self.days:
                int_day = int(day)
                results.append(int_day >= 1 and int_day <= 31)
            return any(results)
        except ValueError:
            return False

    def valid_months(self):
        if self.months == self.any:
            return True
        results = []
        try:
            for month in self.months:
                int_month = int(month)
                results.append(int_month >= 1 and int_month <= 12)
        except ValueError:
            for month in self.months:
                results.append(month.lower() in self.month_codes)
        return any(results)

    def valid_dow(self):
        if self.dow == self.any:
            return True
        results = []
        try:
            for dow in self.dow:
                int_dow = int(dow)
                results.append(int_dow >= 0 and int_dow <= 7)
        except ValueError:
            for dow in self.dow:
                results.append(dow.lower() in self.dow_codes)
        return any(results)
