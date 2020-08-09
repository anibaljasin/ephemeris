import os
from typing import Tuple

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from config.db_config import db
from handlers.ephemeris_handler import EphemerisHandler
from handlers.version_handler import VersionHandler

dir_path = os.path.dirname(os.path.realpath(__file__))


def create_app(db_path: str = None, create_db_schema:bool = True) -> Tuple[Flask, SQLAlchemy]:
    """
    function in charge of creating the flask app and attaching the db instance
    :param db_path: path where the db is located
    :create_db_schema: bool to decide if the app should create the database schema
    :return: a tuple with the flask app instance and the db instance
    """
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

    if create_db_schema:
        with app.app_context():
            db.create_all()

    return app, db


def register_extensions(app: Flask):
    """
    register the db to the app. Other extensions should be added here.
    :param app:
    :return: db instance initialized with the app receive
    """
    db.init_app(app)
    return db
