from rest_framework import serializers
from .models import Car, Tyre


class TyreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tyre
        fields = ['id', 'degradation']


class CarSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField(read_only=True)

    def get_status(self, obj):
        return obj.status

    class Meta:
        model = Car
        fields = ['id', 'status']
