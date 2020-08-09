from datetime import datetime


class EphemerisModel:

    def __init__(self, date: datetime, name: str, id: int):
        self._date = date
        self._name = name
        self._id = id

    def __str__(self):
        return f'{self._name}'

    @property
    def date(self):
        return self._date

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id
