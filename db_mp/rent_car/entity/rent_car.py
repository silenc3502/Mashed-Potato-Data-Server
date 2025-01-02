# from tkinter.constants import INSERT

from django.db import models

class RentCar(models.Model):
    name = models.CharField(max_length=255, unique=True)  # 중복 방지
    car_type = models.CharField(max_length=50)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)


    def __str__(self):
        return (f"ID: {self.id}, Name: {self.name}, Type: {self.car_type}, "
                f"Price per Day: {self.price_per_day}, Availability: {self.availability}")

    class Meta:
        db_table = 'rent_car'


cars = [
    {"name": "Carnival", "car_type": "Van", "price_per_day": 100.00, "availability": True},
    {"name": "K5", "car_type": "Sedan", "price_per_day": 80.00, "availability": True},
    {"name": "Avante", "car_type": "Sedan", "price_per_day": 70.00, "availability": True},
    {"name": "Morning", "car_type": "Compact", "price_per_day": 50.00, "availability": True},
    {"name": "Staria", "car_type": "Van", "price_per_day": 120.00, "availability": True},
    {"name": "Cybertruck", "car_type": "Truck", "price_per_day": 150.00, "availability": True},
    {"name": "GV70", "car_type": "SUV", "price_per_day": 130.00, "availability": True},
    {"name": "G80", "car_type": "Sedan", "price_per_day": 140.00, "availability": True},
]

for car in cars:
    RentCar.objects.create(**car)