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


class Car(models.Model):
    gas_capacity = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
    )
    gas = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
    )
