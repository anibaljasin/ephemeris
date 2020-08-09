from config.db_config import db


class EphemerisRepository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date = db.Column(db.String)

    def __repr__(self):
        return f'id: {self.id}'
