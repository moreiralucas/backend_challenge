from rest_framework import viewsets
from .serializers import CarSerializer, TyreSerializer
from .models import Car, Tyre
from rest_framework.response import Response


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def create(self, _):
        car = Car.createCar()
        serializer = self.get_serializer(car)
        return Response(serializer.data)


class TyreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tyre.objects.all()
    serializer_class = TyreSerializer
