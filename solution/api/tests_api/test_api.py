import json
from api.tests_api.base_test import BaseTest
from django.shortcuts import reverse
from api.views import (CarViewSet, TyreViewSet)
from api.models import Car, Tyre

API_BASE_URL = '/api/v1/'
URL_VIEW_CAR = API_BASE_URL + 'car/'
URL_VIEW_TYRE = API_BASE_URL + 'tyre/'
URL_VIEW_CAR_REFUEL = URL_VIEW_CAR + '{}/refuel/{}/'
URL_VIEW_CAR_MAINTENANCE = URL_VIEW_CAR + '{}/maintenance/{}/'
URL_VIEW_CAR_TRIP = URL_VIEW_CAR + '{}/trip/{}/'

class APITest(BaseTest):
    def test_create_car(self):
        response = self.client.post(URL_VIEW_CAR)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode('utf8'))
        last_created = Car.objects.last()
        self.assertEqual(response['id'], last_created.id)

    def test_retrive_car_status(self):
        response = self.client.post(URL_VIEW_CAR)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode('utf8'))

        status = response['status']
        self.assertTrue(isinstance(status, dict))
        self.assertTrue('gas' in status)
        self.assertEqual('50 Litre(s)', status['gas'])

        self.assertTrue('gas_capacity' in status)
        self.assertEqual(status['gas_capacity'], '50 Litres')

        self.assertTrue('gas_percent' in status)
        self.assertEqual(status['gas_percent'], '100.0%')

        self.assertTrue('tyres' in status)
        tyres = status['tyres']
        self.assertEqual(len(tyres), 4)

    def test_car_refuel(self):
        response = self.client.post(URL_VIEW_CAR)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode('utf8'))

        car_id = response['id']
        response = self.client.post(URL_VIEW_CAR_REFUEL.format(car_id, 20))
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode('utf8'))

    def test_car_maintenance(self):
        response = self.client.post(URL_VIEW_CAR)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode('utf8'))

        car_id = response['id']
        tyres = response['status']['tyres']
        for data in tyres:
            tyre_id = data['id']
            response = self.client.post(URL_VIEW_CAR_MAINTENANCE.format(car_id, tyre_id))
            self.assertEqual(response.status_code, 200)
            status = json.loads(response.content.decode('utf8'))

            self.assertTrue(isinstance(status, dict))
            self.assertTrue('gas' in status)
            self.assertEqual('50 Litre(s)', status['gas'])

            self.assertTrue('gas_capacity' in status)
            self.assertEqual(status['gas_capacity'], '50 Litres')

            self.assertTrue('gas_percent' in status)
            self.assertEqual(status['gas_percent'], '100.0%')

    def test_car_trip(self):
        response = self.client.post(URL_VIEW_CAR)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode('utf8'))

        car_id = response['id']
        response = self.client.post(URL_VIEW_CAR_TRIP.format(car_id, 10000))
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode('utf8'))
