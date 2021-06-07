import logging
from django.http import HttpResponseServerError
from .serializers import CarSerializer, TyreSerializer
from .models import Car, Tyre
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def create(self, _):
        car = Car.createCar()
        serializer = self.get_serializer(car)
        return Response(serializer.data)

    @action(methods=['post'], url_path='(?P<pk>[^/.]+)/refuel/(?P<gas>[^/.]+)', detail=False)
    def refuel(self, request, pk=None, gas=None, *args, **kwargs):
        car = self.get_object()
        try:
            car.refuel(gas)
        except Exception as e:
            logging.info(e)
        serializer = self.get_serializer(car)
        return Response(serializer.data)

    @action(methods=['post'], url_path='(?P<pk>[^/.]+)/maintenance/(?P<id_tyre>[^/.]+)', detail=False)
    def maintenance(self, request, pk=None, id_tyre=None, *args, **kwargs):
        car = self.get_object()
        try:
            tyre = Tyre.objects.get(id=id_tyre)
            status = car.maintenance(tyre)
            return Response(status)
        except Exception as e:
            logging.info(e)

        serializer = self.get_serializer(car)
        return Response(serializer.data)

    @action(methods=['post'], url_path='(?P<pk>[^/.]+)/trip/(?P<distance>[^/.]+)', detail=False)
    def trip(self, request, pk=None, distance=None, *args, **kwargs):
        car = self.get_object()
        try:
            status = car.trip(int(distance))
            return Response(status)
        except Exception as e:
            logging.info(e)

        serializer = self.get_serializer(car)
        return Response(serializer.data)


class TyreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tyre.objects.all()
    serializer_class = TyreSerializer
