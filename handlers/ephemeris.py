import logging
from http import HTTPStatus

from flask_restful import Resource, abort
from flask import request, jsonify

from exceptions.exceptions import MissingParameter, WrongDateFormat
from services.ephemeris import EphemerisService
from utils.date_utils import DateUtil

logger = logging.getLogger(__name__)


class EphemerisHandler(Resource):

    def get(self):
        params = request.args
        day = params.get('day')

        try:
            if day is None:
                raise MissingParameter('day')

            day = DateUtil.validate_date_format(day)
        except (WrongDateFormat, MissingParameter) as ex:
            logger.error(ex)
            abort(HTTPStatus.BAD_REQUEST, message=str(ex))

        month_ephemeris, todays_ephemeris = EphemerisService().get_all_ephemeris(day)

        response = jsonify({
            f'{day.date()}': todays_ephemeris,
            'mes': month_ephemeris,
        })

        return response
