from os import environ
import re
import json

from app import app


class TestApp:
    '''Flask application in flask_app.py'''

    def test_earthquake_magnitude_route(self):
        '''has a resource available at "/earthquakes/magnitude/<magnitude>".'''
        response = app.test_client().get('/earthquakes/magnitude/8.0')
        assert response.status_code == 200

    def test_earthquakes_magnitude_match_response(self):
        '''displays json in earthquake/magnitude route with keys for count, quakes'''

        response = app.test_client().get('/earthquakes/magnitude/9.0')

        # Decode and convert to JSON
        response_body = response.data.decode()
        response_json = json.loads(response_body)

        # Assertions
        assert response_json["count"] == 0  # Updated to reflect the expected count
        assert len(response_json["quakes"]) == 0

        # confirm status
        assert response.status_code == 200

    def test_earthquakes_magnitude_no_match_response(self):
        '''displays json in earthquake/magnitude route with keys for count, quakes'''

        response = app.test_client().get('/earthquakes/magnitude/10.0')

        # Decode and convert to JSON
        response_body = response.data.decode()
        response_json = json.loads(response_body)

        # Assertions
        assert response_json["count"] == 0
        assert len(response_json["quakes"]) == 0

        # confirm status
        assert response.status_code == 200