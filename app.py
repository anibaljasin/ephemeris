import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from handlers.ephemeris import EphemerisHandler
from config.db_config import db

dir_path = os.path.dirname(os.path.realpath(__file__))


def create_app():
    access_control_allow_origin = '*'
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": access_control_allow_origin}})
    api = Api(app)
    api.add_resource(EphemerisHandler, '/efemerides')
    register_extensions(app)
    database_dir = f'sqlite:///{dir_path}/test.db'
    print(database_dir)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_dir
    return app


def register_extensions(app):
    db.init_app(app)


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=4000)
