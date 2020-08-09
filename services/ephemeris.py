from datetime import datetime
from typing import List

from sqlalchemy import and_

from models.ephemeris_model import EphemerisModel
from repository.ephemeris import EphemerisRepository
from utils.date_utils import DateUtil


class EphemerisService:

    def get_all_ephemeris(self, day: datetime):
        first_date_of_month = day.replace(day=1)
        last_day_of_month = DateUtil.get_last_date_of_month(day)
        last_date_of_month = day.replace(day=DateUtil.get_last_date_of_month(day))
        db_ephemeris = EphemerisRepository.query.filter(and_(EphemerisRepository.date >= first_date_of_month,
                                                             EphemerisRepository.date <= last_date_of_month))
        parsed_ephemeris = self.parse_ephemeris(db_ephemeris)
        month_ephemeris, todays_ephemeris = self.build_response(parsed_ephemeris, day, last_day_of_month)

        return month_ephemeris, todays_ephemeris

    def build_response(self, parsed_ephemeris: List[EphemerisModel], day: datetime, last_day_of_month: int):
        todays_ephemeris = {}
        month_ephemeris = {}

        for i in range(1, last_day_of_month + 1):
            key_day = str(i).zfill(2)

            date_to_check = datetime(year=day.year, month=day.month, day=i)
            ephemeris = self.get_ephemeris_by_date(parsed_ephemeris, date_to_check)
            ephemeris_name = str(ephemeris)
            month_ephemeris[key_day] = ephemeris_name
            if day == date_to_check:
                todays_ephemeris = ephemeris_name

        return month_ephemeris, todays_ephemeris

    def get_ephemeris_by_date(self, ephemeris: List[EphemerisModel], date:datetime) -> EphemerisModel:
        for ep in ephemeris:
            if ep.date == date:
                return ep
        return None

    def parse_ephemeris(self, db_ephemeris) -> List[EphemerisModel]:
        if db_ephemeris is None:
            return None

        parsed_ephemeris = []
        for ephemeris in db_ephemeris:
            ep = EphemerisModel(DateUtil.validate_date_format(ephemeris.date), ephemeris.name, ephemeris.id)
            parsed_ephemeris.append(ep)

        return parsed_ephemeris
