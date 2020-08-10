import json
import os
import sqlite3
import unittest
import tempfile
from http import HTTPStatus
from pathlib import Path
from datetime import datetime

import pytest
from parameterized import parameterized

from exceptions.exceptions import WrongDateFormat, MissingParameter, IntegrityError
from server import server


class TestEndpoints(unittest.TestCase):

    def setUp(self) -> None:
        self.tmp_db_dir = str(Path(tempfile.gettempdir()) / f'ephemeris_db_{datetime.now().microsecond}.db')
        self.connection_string = f'sqlite:///{self.tmp_db_dir}'
        open(self.tmp_db_dir, 'w').close()
        app, db = server.create_app(self.connection_string)
        self.db = db
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.set_up_db_dummy_data()
        self.ephemeris_endpoint = '/efemerides'

    def set_up_db_dummy_data(self):
        conn = None
        try:
            conn = sqlite3.connect(self.tmp_db_dir)
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE ephemeris_repository (
                         id INTEGER NOT NULL PRIMARY KEY,
                         name TEXT NOT NULL UNIQUE,
                         date TEXT NOT NULL)''')

            cursor.execute('''INSERT INTO ephemeris_repository VALUES
            (1, "dia del metegol", "2020-01-01"),
            (2, "dia del amigo", "2020-07-20"),
            (3, "dia del hermano", "2020-08-11"),
            (4, "dia del padre", "2020-09-15"),
            (5, "dia del futbol", "2020-06-24")''')

            conn.commit()

        except Exception as ex:
            print(f"Error during db creation: {ex}")
            conn.rollback()
        finally:
            conn.close()

    def tearDown(self):
        os.remove(self.tmp_db_dir)

    @parameterized.expand([
        ('2020-01-10', 31),
        ('2020-02-10', 29),
        ('2020-03-15', 31),
        ('2020-04-10', 30),
        ('2020-05-01', 31),
        ('2020-06-27', 30),
        ('2020-07-10', 31),
        ('2020-08-10', 31),
        ('2020-09-17', 30),
        ('2020-10-29', 31),
        ('2020-11-17', 30),
        ('2020-12-29', 31),
    ])
    def test_ephemeris_passing_right_date(self, day_to_check, expected_month_length):
        endpoint = self.ephemeris_endpoint
        key_param = 'day'
        url = f'{endpoint}?{key_param}={day_to_check}'
        response = self.app.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(day_to_check in response.json)
        self.assertTrue('mes' in response.json)
        self.assertTrue(len(response.json['mes']) == expected_month_length)

    @parameterized.expand([
        '01-10-2020',
        '14-10-2020',
        '01/10/2020',
        '16/10/2020',
    ])
    def test_passing_wrong_date_format(self, wrong_date_format):
        endpoint = self.ephemeris_endpoint
        key_param = 'day'
        url = f'{endpoint}?{key_param}={wrong_date_format}'

        def make_request(): self.app.get(url)
        self.assertRaises(WrongDateFormat, make_request())

    def test_passing_wrong_query_param(self):
        endpoint = self.ephemeris_endpoint
        wrong_key_param = 'wrong_key'
        valid_date = '2020-10-10'
        url = f'{endpoint}?{wrong_key_param}={valid_date}'

        def make_request(): self.app.get(url)

        self.assertRaises(MissingParameter, make_request())

    def test_add_new_ephemeris_with_valid_data(self):
        new_ephemeris = {"name": "dia del murcielago", "date": "2020-12-12"}
        endpoint = self.ephemeris_endpoint
        response = self.app.post(endpoint, data=json.dumps(new_ephemeris), content_type='application/json')

        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_json = json.loads(response.data)

        self.assertIsNotNone(response_json["ephemeris"])
        self.assertEqual(response_json["ephemeris"]["name"], new_ephemeris["name"])
        self.assertEqual(response_json["ephemeris"]["date"], new_ephemeris["date"])

    def test_add_new_ephemeris_with_missing_date_parameter(self):
        new_ephemeris = {"name": "dia de la camiseta"}
        endpoint = self.ephemeris_endpoint

        def make_request(): self.app.post(endpoint, data=json.dumps(new_ephemeris), content_type='application/json')

        self.assertRaises(MissingParameter, make_request)

    def test_put_method_not_allowed(self):
        endpoint = self.ephemeris_endpoint
        key_param = 'day'
        url = f'{endpoint}?{key_param}=2020-10-01'

        response = self.app.put(url)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_delete_method_not_allowed(self):
        endpoint = self.ephemeris_endpoint
        key_param = 'day'
        url = f'{endpoint}?{key_param}=2020-10-01'

        response = self.app.delete(url)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_patch_method_not_allowed(self):
        endpoint = self.ephemeris_endpoint
        key_param = 'day'
        url = f'{endpoint}?{key_param}=2020-10-01'

        response = self.app.patch(url)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_server_is_up_and_running(self):
        response = self.app.get('/version', follow_redirects=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)

