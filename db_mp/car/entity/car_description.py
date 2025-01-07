from django.db import models

from car.entity.car import Car


class CarDescription(models.Model):
    id = models.AutoField(primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="descriptions")
    description = models.TextField()

    class Meta:
        db_table = 'car_description'
        app_label = 'car'

    def __str__(self):
        return f"CarDescription(id={self.id}, description={self.description})"

    def getDescription(self):
        return self.description
