from django.test import TestCase
from rest_framework.test import APIClient
from api.models import Car

class BaseTest(TestCase):

    def setUp(self):
        self.car = Car.createCar()
        self.client = APIClient()

    def tearDown(self):
        pass
