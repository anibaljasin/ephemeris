import calendar
from datetime import datetime

from exceptions.exceptions import WrongDateFormat


class DateUtil:

    @staticmethod
    def validate_date_format(date: str, required_format: str = '%Y-%m-%d') -> datetime:
        """
        Validate the date format needed. Will raise WrongDateFormat if the date is not
        in the specified format.
        :param date: string with date
        :param required_format: format to validate
        :return: a datetime object with the date parsed
        """
        try:
            date = datetime.strptime(date, required_format)
        except ValueError:
            raise WrongDateFormat()

        return date

    @staticmethod
    def get_last_date_of_month(date: datetime) -> int:
        """
        return the last day of month of the datetime received
        :param date: datetime object to extract the month
        :return: int with the last day of the month. eg. 31 for December.
        """
        _, last_day = calendar.monthrange(date.year, date.month)
        return last_day
