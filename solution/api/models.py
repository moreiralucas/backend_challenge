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

    @property
    def status(self):
        return {'id': self.id, 'degradation': self.degradation}

    def increment_degradation(self, value=1):
        self.degradation += value
        self.save()


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

    def gas_decrement(self, value=1):
        self.gas = int(self.gas) - value
        self.save()

    def maintenance(self, part_to_replace):
        if isinstance(part_to_replace, Tyre):
            tyre = self.tyre.filter(
                degradation_gt=95, pk=part_to_replace.pk
            ).first()
            if tyre is not None:
                tyre.delete()
                Tyre.createTyre(self)
            return self

    def refuel(self, gas_quantity):
        assert self.gas_percent >= 5, f'The car should NOT be refueled before it has less than 5% gas on tank!'
        if self.gas + gas_quantity > self.gas_capacity:
            only_used = self.gas_capacity - self.gas
            self.gas = self.gas_capacity
            logging.info(
                f'The amount of gas exceeded the limit supported by the car, only {only_used} liters were used.')
        else:
            self.gas = gas_quantity
        self.save()
