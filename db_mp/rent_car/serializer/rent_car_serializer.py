from rest_framework import serializers
from rent_car.entity.rent_car import RentCar

class RentCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentCar
        fields = ['name', 'car_type', 'price_per_day', 'availability']



