import json
import logging
from http import HTTPStatus

from flask_restful import Resource, abort
from flask import request, jsonify

from exceptions.exceptions import MissingParameter, WrongDateFormat
from services.ephemeris_service import EphemerisService
from utils.date_utils import DateUtil

logger = logging.getLogger(__name__)


class EphemerisHandler(Resource):

    def __init__(self):
        self._ephemeris_svc = EphemerisService()

    def post(self):
        """
        Method responsible to handle the http post request. It is used to insert new ephemeris.
        :return: the saved ephemeris or an error if it couldn't
        """
        body = json.loads(request.data)
        if "name" not in body or "date" not in body:
            raise MissingParameter("name and date")

        name = body["name"]
        date = body["date"]

        try:
            DateUtil.validate_date_format(body["date"])
        except WrongDateFormat as ex:
            logger.error(ex)
            abort(HTTPStatus.BAD_REQUEST, message=str(ex))

        ephemeris = None
        try:
            ephemeris = self._ephemeris_svc.create_ephemeris(name=name, date=date)
        except Exception as ex:
            logger.error(ex)
            abort(HTTPStatus.BAD_REQUEST, message=str(ex))

        response = {"ephemeris": ephemeris}
        return response

    def get(self):
        """
        Method that receives the http get requests in charge of finding the ephemeris from the 'day' query param
        passed, the 'day' query param is mandatory otherwise will raise MissingParameter exception.
        :return: the ephemeris from the day passed and the monthly ephemeris.
        """
        params = request.args
        day = params.get('day')

        try:
            if day is None:
                raise MissingParameter('day')

            day = DateUtil.validate_date_format(day)
        except (WrongDateFormat, MissingParameter) as ex:
            logger.error(ex)
            abort(HTTPStatus.BAD_REQUEST, message=str(ex))

        month_ephemeris, todays_ephemeris = self._ephemeris_svc.get_ephemeris_from_month(day)

        response = jsonify({
            f'{day.date()}': todays_ephemeris,
            'mes': month_ephemeris,
        })

        return response
