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
        return {'id': self.pk, 'degradation': self.degradation}

    def increment_degradation(self, value=1):
        self.degradation += value
        self.save()


class Car(models.Model):
    _gas_capacity = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
    )
    _gas = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
    )

    @property
    def gas(self):
        return int(self._gas)

    @property
    def gas_capacity(self):
        return int(self._gas_capacity)

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
        """Returns a new car instance

        Returns:
            Car: Car instance
        """
        car = cls.objects.create(
            _gas_capacity=CAR_GAS_CAPACITY,
            _gas=CAR_GAS_CAPACITY)
        for _ in range(4):
            Tyre.objects.create(car=car)
        return car

    def gas_decrement(self, value=1):
        """Decreases car gas.

        Args:
            value (int, optional): The decrement step value. Defaults to 1.
        """
        self._gas = self.gas - value
        self.save()

    def maintenance(self, part_to_replace):
        """Carries out maintenance on the car and returns its instance.

        Args:
            part_to_replace (Model): Element of the car that will be serviced.

        Returns:
            Car: Car instance
        """
        if isinstance(part_to_replace, Tyre):
            tyre = self.tyre.filter(
                degradation__gt=TYRE_NEED_MAINTENANCE, pk=part_to_replace.pk
            ).first()
            if tyre is not None:
                tyre.delete()
                Tyre.createTyre(self)
        return self.status

    def refuel(self, gas_quantity):
        """Fuel up the car if possible

        Args:
            gas_quantity (int): Number of liters of gasoline that will fuel the car
        """
        assert self.gas_percent < 5, f'The car should NOT be refueled before it has less than 5% gas on tank!\nActually you have {self.gas_percent}% of gas'
        if self.gas + gas_quantity > self.gas_capacity:
            only_used = self.gas_capacity - self.gas
            self._gas = self.gas_capacity
            logging.info(
                f'The amount of gas exceeded the limit supported by the car, only {only_used} liters were used.')
        else:
            self._gas = gas_quantity
        self.save()

    def tyres_increment_degradation(self):
        """Increment of the degradation of the 4 tires of the car.
        """
        for t in self.tyre.all():
            t.increment_degradation()

    def trip(self, distance):
        """Performs the trip and returns the status of the car after the trip.

        Args:
            distance (int): Distance to be covered by the car on the trip in km

        Returns:
            dict: Car status after trip.
        """
        assert distance >= 0, 'The distance can\'t have a negative value!'
        travelled_distance = 0
        while travelled_distance < distance:
            if travelled_distance % 8 == 0:
                self.gas_decrement()

            if travelled_distance % 3 == 0:
                self.tyres_increment_degradation()

            if self.gas_percent < 5:
                self.refuel(self.gas_capacity * 0.95)

            for t in self.tyre.all():
                self.maintenance(t)
            travelled_distance += 1

        return self.status
