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

    @action(methods=['post'], url_path='(?P<pk>[^/.]+)/refuel', detail=False)
    def refuel(self, request, pk=None, *args, **kwargs):
        car = self.get_object()
        if car and 'gas_quantity' in request.POST:
            gas_quantity = request.POST['gas_quantity']
            car.refuel(gas_quantity)
        serializer = self.get_serializer(car)
        return Response(serializer.data)


class TyreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tyre.objects.all()
    serializer_class = TyreSerializer
