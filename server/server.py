import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from config.db_config import db
from handlers.ephemeris_handler import EphemerisHandler
from handlers.version_handler import VersionHandler

dir_path = os.path.dirname(os.path.realpath(__file__))


def create_app(db_path=None):
    access_control_allow_origin = '*'
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": access_control_allow_origin}})
    api = Api(app)
    api.add_resource(VersionHandler, '/version')
    api.add_resource(EphemerisHandler, '/efemerides')
    db = register_extensions(app)

    if db_path is None:
        project_dir = os.getcwd()
        db_path = f'sqlite:///{project_dir}/test.db'

    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    return app, db


def register_extensions(app):
    db.init_app(app)
    return db
