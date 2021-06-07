import logging
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from carmanager.settings import (
    TYRE_NEED_MAINTENANCE,
    CAR_GAS_CAPACITY
)


class Tyre(models.Model):
    degradation = models.PositiveSmallIntegerField(
        default=0
    )
    car = models.ForeignKey(
        'api.Car',
        models.CASCADE,
        related_name='tyre'
    )

    @classmethod
    def createTyre(cls, car):
        tyres = cls.objects.filter(car=car).count()
        assert tyres <= 4, 'A car can\'t have more than 4 tyres!'
        return cls.objects.create(car=car)


class Car(models.Model):
    gas_capacity = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
    )
    gas = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
    )

    @property
    def gas_percent(self):
        return 0 if self.gas == 0 else self.gas / self.gas_capacity * 100

    @property
    def status(self):
        return {
            'gas': f'{self.gas} Litre(s)',
            'gas_capacity': f'{self.gas_capacity} Litres',
            'gas_percent': f'{self.gas_percent}%',
            'tyres': [t.status for t in self.tyre.all()]
        }

    @classmethod
    def createCar(cls):
        car = cls.objects.create(
            gas_capacity=CAR_GAS_CAPACITY,
            gas=CAR_GAS_CAPACITY)
        for _ in range(4):
            Tyre.objects.create(car=car)
        return car
