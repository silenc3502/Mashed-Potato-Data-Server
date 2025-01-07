from django.db import models

from car.entity.car import Car


class CarImage(models.Model):
    id = models.AutoField(primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="images")
    image = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'car_image'
        app_label = 'car'

    def __str__(self):
        return f"CarImage(id={self.id}, image={self.image})"

    def getImage(self):
        return self.image
