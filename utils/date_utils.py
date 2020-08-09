import calendar
from datetime import datetime

from exceptions.exceptions import WrongDateFormat


class DateUtil:

    @staticmethod
    def validate_date_format(date: str) -> datetime:
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise WrongDateFormat()

        return date

    @staticmethod
    def get_last_date_of_month(date: datetime) -> int:
        _, last_day = calendar.monthrange(date.year, date.month)
        return last_day
