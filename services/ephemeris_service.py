from datetime import datetime
from typing import List, Tuple, Dict

from flask_sqlalchemy import BaseQuery
from sqlalchemy import and_

from models.ephemeris_model import EphemerisModel
from repository.ephemeris_repository import EphemerisRepository
from utils.date_utils import DateUtil


class EphemerisService:

    def get_ephemeris_from_month(self, day: datetime) -> Tuple[Dict[str, str], Dict[str, str]]:
        """
        Responsible to query and format the ephemeris from the month of the day received
        :param day: datetime object with the day to use
        :return:
        """
        first_date_of_month = day.replace(day=1)
        last_day_of_month = DateUtil.get_last_date_of_month(day)
        last_date_of_month = day.replace(day=DateUtil.get_last_date_of_month(day))
        db_ephemeris = EphemerisRepository.query.filter(and_(EphemerisRepository.date >= first_date_of_month,
                                                             EphemerisRepository.date <= last_date_of_month))
        parsed_ephemeris = self._parse_ephemeris(db_ephemeris)
        month_ephemeris, todays_ephemeris = self._build_response(parsed_ephemeris, day, last_day_of_month)

        return month_ephemeris, todays_ephemeris

    def _build_response(self, parsed_ephemeris: List[EphemerisModel], day: datetime, last_day_of_month: int) -> \
            Tuple[Dict[str, str], Dict[str, str]]:
        """
        Reponsible to create two dictionaries containing the ephemeris from the day received and the other one with
        the monthly ephemeris
        :param parsed_ephemeris: list of ephemeris to retrived
        :param day: date to check for ephemeris
        :param last_day_of_month: last day of the day to check
        :return: a dict with the day's ephemeris and other with the monthly ephemeris
        """
        todays_ephemeris = {}
        month_ephemeris = {}

        for i in range(1, last_day_of_month + 1):
            key_day = str(i).zfill(2)

            date_to_check = datetime(year=day.year, month=day.month, day=i)
            ephemeris = self._get_ephemeris_by_date(parsed_ephemeris, date_to_check)
            ephemeris_name = str(ephemeris)
            month_ephemeris[key_day] = ephemeris_name
            if day == date_to_check:
                todays_ephemeris = str(ephemeris_name)

        return month_ephemeris, todays_ephemeris

    def _get_ephemeris_by_date(self, ephemeris: List[EphemerisModel], date: datetime) -> EphemerisModel:
        """
        Look for the ephemeris with the date receive. Will return None if none of the ephemeris has that date.
        :param ephemeris: List of ephemeris
        :param date: the date we want an ephemeris to have.
        :return: the ephemeris with 'date' or None
        """
        for ep in ephemeris:
            if ep.date == date:
                return ep
        return None

    def _parse_ephemeris(self, db_ephemeris: BaseQuery) -> List[EphemerisModel]:
        """
        Method responsible to create a list of EphemerisModel from the result of the query made to the database.
        :param db_ephemeris: result of the query to the database
        :return: list of EphemerisModel
        """
        if db_ephemeris is None:
            return None

        parsed_ephemeris = []
        for ephemeris in db_ephemeris:
            ep = EphemerisModel(DateUtil.validate_date_format(ephemeris.date), ephemeris.name, ephemeris.id)
            parsed_ephemeris.append(ep)

        return parsed_ephemeris
