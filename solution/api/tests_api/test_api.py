import json
from api.tests_api.base_test import BaseTest
from django.shortcuts import reverse
from api.views import (CarViewSet, TyreViewSet)
from api.models import Car, Tyre

API_BASE_URL = '/api/v1/'
URL_VIEW_CAR = API_BASE_URL + 'car/'
URL_VIEW_TYRE = API_BASE_URL + 'tyre/'


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
        self.assertTrue('gas_capacity' in status)
        self.assertTrue('gas_percent' in status)
        self.assertTrue('tyres' in status)
        tyres = status['tyres']
        self.assertEqual(len(tyres), 4)

