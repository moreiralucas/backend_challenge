from api.tests_api.base_test import BaseTest
from api.models import Car, Tyre
from django.test.utils import override_settings


class CarTest(BaseTest):

    @override_settings(TYRE_NEED_MAINTENANCE=94, CAR_GAS_CAPACITY=50)
    def test_create_car_with_success(self):
        car = Car.createCar()
        self.assertTrue(isinstance(car, Car))
        self.assertEqual(car.gas, 50)

    def test_car_decrement_gas_by_one_value(self):
        gas = int(self.car.gas - 1)
        self.car.gas_decrement()
        self.assertEqual(gas, int(self.car.gas))

    def test_car_cant_swape_tyre_before_94_degradation(self):
        car = self.car
        tyre = car.tyre.first()
        response_car = car.maintenance(tyre)
        tyre_dict = {'id': tyre.pk, 'degradation': tyre.degradation}
        self.assertIn(tyre_dict, response_car['tyres'])

    # def test_car_should_not_refuel_before_it_has_less_than_5_on_tank(self):
    #     car = self.car
    #     car.refuel(20)

    def test_tyres_increment_degradation(self):
        self.car.tyres_increment_degradation()
        self.car.tyres_increment_degradation()

        for t in self.car.tyre.all():
            self.assertEqual(t.degradation, 2)

    def test_trip_with_successful(self):
        self.car.trip(10000)
