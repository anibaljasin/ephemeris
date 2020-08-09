import logging

from sqlalchemy import exc

from config.db_config import db
from exceptions.exceptions import IntegrityError

logger = logging.getLogger(__name__)


class EphemerisRepository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date = db.Column(db.String)

    def save(self):
        """
        Method responsible the create a new record in the database with the data of the instance.
        :return:
        """
        try:
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError as ex:
            logger.error(str(ex))
            msg = f'Duplicate name "{self.name}" already inserted in the database'
            raise IntegrityError(msg=msg)

    def __repr__(self):
        return f'id: {self.id}'
