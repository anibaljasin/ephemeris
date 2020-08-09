
class MissingParameter(Exception):
    def __init__(self, missing_param=None):
        msg = f'Missing parameter {missing_param}'
        super(MissingParameter, self).__init__(msg)


class WrongDateFormat(Exception):
    def __init__(self):
        msg = 'Incorrect date format, should be YYYY-MM-DD'
        super(WrongDateFormat, self).__init__(msg)


class EphemerisParseError(Exception):
    def __init__(self):
        msg = 'Error while parsing the retrived Ephemeris'
        super(EphemerisParseError, self).__init__(msg)


class IntegrityError(Exception):
    def __init__(self, msg=''):
        super(IntegrityError, self).__init__(msg)
