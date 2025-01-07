from django.db import models

from car.entity.car import Car


class CarPrice(models.Model):
    id = models.AutoField(primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="prices")
    price = models.IntegerField()

    class Meta:
        db_table = 'car_price'
        app_label = 'car'

    def __str__(self):
        return f"CarPrice(id={self.id}, price={self.price})"

    def getPrice(self):
        return self.price
