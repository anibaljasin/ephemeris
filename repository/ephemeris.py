from config import db_config


class EphemerisRepository(db_config.db.Model):
    id = db_config.db.Column(db_config.db.Integer, primary_key=True)
    name = db_config.db.Column(db_config.db.String)
    date = db_config.db.Column(db_config.db.String)

    def __repr__(self):
        return f'id: {self.id}'
